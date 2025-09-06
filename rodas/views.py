from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import PacienteRegisterForm, SolicitaCorridaform
from .models import Usuario, Paciente, TipoUsuario, Corrida, CorridaStatus, Motorista


# Create your views here.


def index(request):
    """
    View para a página inicial do app rodas.
    """
    context = {
        "title": "Esperança Sobre Rodas - Início",
    }
    return render(request, "rodas/index.html", context)


def sobre(request):
    """
    View para a página sobre o projeto.
    """
    context = {
        "title": "Sobre - Esperança Sobre Rodas",
    }
    return render(request, "rodas/sobre.html", context)


def contato(request):
    """
    View para a página de contato.
    """
    if request.method == "POST":
        # Processar o formulário de contato
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        assunto = request.POST.get("assunto")
        mensagem = request.POST.get("mensagem")

        # Aqui você pode adicionar a lógica para salvar no banco de dados
        # ou enviar por email

        messages.success(
            request,
            "Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.",
        )

    context = {
        "title": "Contato - Esperança Sobre Rodas",
    }
    return render(request, "rodas/contato.html", context)


def login_view(request):
    """
    View para login de usuários.
    """
    if request.user.is_authenticated:
        return redirect("rodas:dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f"Bem-vindo(a), {user.nome_completo or user.email}!"
            )
            next_url = request.GET.get("next", "rodas:dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    context = {
        "title": "Login - Esperança Sobre Rodas",
    }
    return render(request, "rodas/auth/login.html", context)


def logout_view(request):
    """
    View para logout de usuários.
    """
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect("rodas:index")


def register_view(request):
    """
    View para registro de novos usuários.
    """
    if request.user.is_authenticated:
        return redirect("rodas:dashboard")

    if request.method == "POST":
        form = PacienteRegisterForm(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                nome_completo=form.cleaned_data["nome_completo"],
                cpf=form.cleaned_data["cpf"],
                tipo_usuario="paciente",
                ativo=True,
                telefone="",  # Pode ser adicionado ao formulário se necessário
            )
            Paciente.objects.create(
                usuario=usuario,
                responsavel_nome=form.cleaned_data["responsavel_nome"],
                responsavel_cpf=form.cleaned_data["responsavel_cpf"],
                responsavel_telefone=form.cleaned_data["responsavel_telefone"],
                necessita_cadeira_rodas=form.cleaned_data["necessita_cadeira_rodas"],
                imunossuprimido=form.cleaned_data["imunossuprimido"],
                observacoes_medicas=form.cleaned_data["observacoes_medicas"],
                aceite_termos=form.cleaned_data["aceite_termos"],
                data_aceite_termos=timezone.now(),
            )
            messages.success(
                request, "Conta criada com sucesso! Faça login para continuar."
            )
            return redirect("rodas:login")
    else:
        form = PacienteRegisterForm()

    context = {
        "title": "Registro - Esperança Sobre Rodas",
        "form": form,
    }
    return render(request, "rodas/paciente/register.html", context)


def password_reset_view(request):
    """
    View para solicitar reset de senha.
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name="rodas/auth/password_reset_email.html",
                html_email_template_name="rodas/auth/password_reset_email.html",
                subject_template_name="rodas/auth/password_reset_subject.txt",
                from_email="noreply@esperancasobrerodas.org",
            )
            messages.success(
                request,
                "Instruções para redefinir sua senha foram enviadas para seu email.",
            )
            return redirect("rodas:login")
    else:
        form = PasswordResetForm()

    context = {
        "title": "Esqueceu a Senha - Esperança Sobre Rodas",
        "form": form,
    }
    return render(request, "rodas/auth/password_reset.html", context)


@login_required
def dashboard_view(request):
    """
    View do dashboard - exemplo de área restrita.
    """
    usuario: Usuario = request.user

    if usuario.tipo_usuario == TipoUsuario.PACIENTE:
        paciente = Paciente.objects.get(usuario=usuario)

        corridas = (
            Corrida.objects.filter(paciente=paciente).order_by("-data_hora_agendada")
            if paciente
            else []
        )

        return render(request, "rodas/paciente/dashboard.html", {
            "title": "Dashboard - Esperança Sobre Rodas",
            "user": usuario,
            "corridas": corridas,
        })

    return render(request, "rodas/motorista/dashboard.html", {
        "title": "Dashboard - Esperança Sobre Rodas",
        "user": usuario,
    })


@login_required
def solicitar_corrida_view(request):
    """
    View para solicitar uma corrida - exemplo de funcionalidade para pacientes.
    """
    user: Usuario = request.user

    if user.tipo_usuario != TipoUsuario.PACIENTE:
        messages.error(request, "Apenas pacientes podem solicitar corridas.")
        return redirect("rodas:dashboard")

    context = {
        "title": "Solicitar Corrida - Esperança Sobre Rodas",
        "form": None,
    }

    if request.method == "POST":
        form = SolicitaCorridaform(request.POST)
        if form.is_valid():
            corrida = Corrida()
            corrida.paciente = Paciente.objects.get(usuario=user)
            corrida.endereco_origem = form.cleaned_data["endereco_origem"]
            corrida.endereco_destino = form.cleaned_data["endereco_destino"]
            corrida.status = CorridaStatus.PENDENTE

            data_agendamento = form.cleaned_data["data_agendamento"]
            hora_agendamento = form.cleaned_data["hora_agendamento"]
            data_hora_agendada = timezone.datetime.combine(
                data_agendamento, hora_agendamento
            )
            corrida.data_hora_agendada = data_hora_agendada

            corrida.save()
            messages.success(request, "Sua corrida foi solicitada com sucesso!")
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
            context["form"] = form
    else:
        initial_data = {
            "endereco_origem": request.GET.get("endereco_origem", ""),
            "endereco_destino": request.GET.get("endereco_destino", ""),
            "data_agendamento": request.GET.get("data_agendamento", ""),
            "hora_agendamento": request.GET.get("hora_agendamento", ""),
        }
        form = SolicitaCorridaform(initial=initial_data)
        context["form"] = form

    return render(request, "rodas/paciente/solicita_corrida.html", context)


@login_required
def profile_view(request):
    """
    View do perfil do usuário - exemplo de área restrita.
    """
    context = {
        "title": "Meu Perfil - Esperança Sobre Rodas",
        "user": request.user,
    }
    return render(request, "rodas/profile.html", context)
