from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .forms import PacienteRegisterForm, MotoristaRegisterForm, SolicitaCorridaform
from .models import (
    Usuario,
    Paciente,
    TipoUsuario,
    Corrida,
    CorridaStatus,
    Motorista,
    Notificacao,
)


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


def register_motorista_view(request):
    """
    View para registro de motoristas voluntários.
    """
    if request.user.is_authenticated:
        return redirect("rodas:dashboard")

    if request.method == "POST":
        form = MotoristaRegisterForm(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                nome_completo=form.cleaned_data["nome_completo"],
                cpf=form.cleaned_data["cpf"],
                telefone=form.cleaned_data["telefone"],
                tipo_usuario="motorista",
                ativo=True,
            )
            Motorista.objects.create(
                usuario=usuario,
                marca_veiculo=form.cleaned_data["marca_veiculo"],
                modelo_veiculo=form.cleaned_data["modelo_veiculo"],
                cor_veiculo=form.cleaned_data["cor_veiculo"],
                ano_veiculo=form.cleaned_data.get("ano_veiculo"),
                placa_veiculo=form.cleaned_data.get("placa_veiculo", ""),
                cnh_numero=form.cleaned_data.get("cnh_numero", ""),
                cnh_validade=form.cleaned_data.get("cnh_validade"),
                aceite_termos_voluntariado=form.cleaned_data[
                    "aceite_termos_voluntariado"
                ],
                data_aceite_termos=timezone.now(),
                status_aprovacao="pendente",
            )
            messages.success(
                request,
                "Cadastro realizado com sucesso! Seu perfil será analisado pela administração.",
            )
            return redirect("rodas:login")
    else:
        form = MotoristaRegisterForm()

    context = {
        "title": "Cadastro de Motorista - Esperança Sobre Rodas",
        "form": form,
    }
    return render(request, "rodas/motorista/register.html", context)


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

        # Calcular estatísticas
        total_corridas = corridas.count()
        corridas_concluidas = corridas.filter(status=CorridaStatus.CONCLUIDA).count()
        corridas_pendentes = corridas.filter(status=CorridaStatus.PENDENTE).count()

        return render(
            request,
            "rodas/paciente/dashboard.html",
            {
                "title": "Dashboard - Esperança Sobre Rodas",
                "user": usuario,
                "corridas": corridas,
                "total_corridas": total_corridas,
                "corridas_concluidas": corridas_concluidas,
                "corridas_pendentes": corridas_pendentes,
            },
        )

    # Para motoristas
    if usuario.tipo_usuario == TipoUsuario.MOTORISTA:
        try:
            motorista = Motorista.objects.get(usuario=usuario)

            # Corridas pendentes (sem motorista atribuído)
            corridas_pendentes = Corrida.objects.filter(
                status=CorridaStatus.PENDENTE, motorista__isnull=True
            ).order_by("data_hora_agendada")[:10]

            # Corridas do motorista
            corridas_motorista = Corrida.objects.filter(motorista=motorista).order_by(
                "-data_hora_agendada"
            )

            return render(
                request,
                "rodas/motorista/dashboard.html",
                {
                    "title": "Dashboard Motorista - Esperança Sobre Rodas",
                    "user": usuario,
                    "corridas_pendentes": corridas_pendentes,
                    "corridas_motorista": corridas_motorista,
                },
            )
        except Motorista.DoesNotExist:
            # Se não tem perfil de motorista, redireciona para criar
            messages.error(request, "Perfil de motorista não encontrado.")
            return redirect("rodas:register_motorista")

    return render(
        request,
        "rodas/motorista/dashboard.html",
        {
            "title": "Dashboard - Esperança Sobre Rodas",
            "user": usuario,
        },
    )


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
        "success": False,
    }

    if request.method == "POST":
        form = SolicitaCorridaform(request.POST)
        if form.is_valid():
            try:
                corrida = Corrida()
                corrida.paciente = Paciente.objects.get(usuario=user)
                corrida.endereco_origem = form.cleaned_data["endereco_origem"]
                corrida.endereco_destino = form.cleaned_data["endereco_destino"]
                corrida.status = CorridaStatus.PENDENTE
                corrida.tem_acompanhante = form.cleaned_data.get(
                    "tem_acompanhante", False
                )
                corrida.necessita_cadeira_rodas = form.cleaned_data.get(
                    "necessita_cadeira_rodas", False
                )
                corrida.observacoes = form.cleaned_data.get("observacoes", "")

                data_agendamento = form.cleaned_data["data_agendamento"]
                hora_agendamento = form.cleaned_data["hora_agendamento"]
                data_hora_agendada = timezone.datetime.combine(
                    data_agendamento, hora_agendamento
                )
                corrida.data_hora_agendada = data_hora_agendada

                corrida.save()

                messages.success(request, "Sua corrida foi solicitada com sucesso!")
                context["success"] = True
                # Limpar o formulário após sucesso
                form = SolicitaCorridaform()
                context["form"] = form

            except Exception:
                messages.error(request, "Erro ao solicitar corrida. Tente novamente.")
                context["form"] = form
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


@login_required
def corrida_detalhes_view(request, corrida_id):
    """
    View para visualizar detalhes de uma corrida específica.
    """
    corrida = get_object_or_404(Corrida, id=corrida_id)
    user = request.user

    # Verificar se o usuário tem permissão para ver esta corrida
    if user.tipo_usuario == TipoUsuario.MOTORISTA:
        # Motoristas podem ver corridas pendentes ou suas próprias corridas
        if (
            corrida.status != CorridaStatus.PENDENTE
            and corrida.motorista != user.perfil_motorista
        ):
            messages.error(request, "Você não tem permissão para ver esta corrida.")
            return redirect("rodas:dashboard")
    elif user.tipo_usuario == TipoUsuario.PACIENTE:
        # Pacientes só podem ver suas próprias corridas
        if corrida.paciente != user.perfil_paciente:
            messages.error(request, "Você não tem permissão para ver esta corrida.")
            return redirect("rodas:dashboard")
    else:
        messages.error(request, "Acesso negado.")
        return redirect("rodas:dashboard")

    context = {
        "title": f"Corrida #{corrida.id} - Esperança Sobre Rodas",
        "corrida": corrida,
        "user": user,
    }

    if user.tipo_usuario == TipoUsuario.MOTORISTA:
        return render(request, "rodas/motorista/corrida_detalhes.html", context)
    else:
        return render(request, "rodas/paciente/corrida_detalhes.html", context)


@login_required
@require_http_methods(["POST"])
def aceitar_corrida_view(request, corrida_id):
    """
    API endpoint para motorista aceitar uma corrida.
    """
    if request.user.tipo_usuario != TipoUsuario.MOTORISTA:
        return JsonResponse(
            {"success": False, "message": "Apenas motoristas podem aceitar corridas."}
        )

    try:
        motorista = request.user.perfil_motorista

        # Verificar se o motorista está aprovado e online
        if motorista.status_aprovacao != "aprovado":
            return JsonResponse(
                {"success": False, "message": "Seu cadastro ainda não foi aprovado."}
            )

        if not motorista.online:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Você precisa estar online para aceitar corridas.",
                }
            )

        corrida = get_object_or_404(Corrida, id=corrida_id)

        # Verificar se a corrida pode ser aceita
        if not corrida.pode_ser_aceita:
            return JsonResponse(
                {"success": False, "message": "Esta corrida não pode mais ser aceita."}
            )

        # Aceitar a corrida
        corrida.motorista = motorista
        corrida.status = CorridaStatus.ACEITA
        corrida.data_hora_aceite = timezone.now()
        corrida.save()

        # Criar notificação para o paciente
        Notificacao.objects.create(
            usuario=corrida.paciente.usuario,
            tipo="corrida_aceita",
            titulo="Corrida aceita!",
            mensagem=f"O motorista {motorista.usuario.get_short_name()} aceitou sua corrida.",
            corrida=corrida,
        )

        return JsonResponse(
            {
                "success": True,
                "message": "Corrida aceita com sucesso!",
                "redirect_url": f"/corrida/{corrida.id}/",
            }
        )

    except Exception:
        return JsonResponse(
            {"success": False, "message": "Erro interno. Tente novamente."}
        )


@login_required
@require_http_methods(["POST"])
def toggle_motorista_status_view(request):
    """
    API endpoint para alternar status online/offline do motorista.
    """
    if request.user.tipo_usuario != TipoUsuario.MOTORISTA:
        return JsonResponse(
            {"success": False, "message": "Apenas motoristas podem alterar status."}
        )

    try:
        motorista = request.user.perfil_motorista

        # Verificar se o motorista está aprovado
        if motorista.status_aprovacao != "aprovado":
            return JsonResponse(
                {"success": False, "message": "Seu cadastro ainda não foi aprovado."}
            )

        # Alternar status
        motorista.online = not motorista.online
        motorista.save()

        status_text = "online" if motorista.online else "offline"
        return JsonResponse(
            {
                "success": True,
                "message": f"Status alterado para {status_text}.",
                "online": motorista.online,
            }
        )

    except Exception:
        return JsonResponse(
            {"success": False, "message": "Erro interno. Tente novamente."}
        )


@login_required
@require_http_methods(["POST"])
def atualizar_status_corrida_view(request, corrida_id):
    """
    API endpoint para atualizar status da corrida (iniciar, marcar chegada, finalizar).
    """
    if request.user.tipo_usuario != TipoUsuario.MOTORISTA:
        return JsonResponse(
            {
                "success": False,
                "message": "Apenas motoristas podem atualizar status da corrida.",
            }
        )

    try:
        data = json.loads(request.body)
        novo_status = data.get("status")

        corrida = get_object_or_404(Corrida, id=corrida_id)
        motorista = request.user.perfil_motorista

        # Verificar se é o motorista da corrida
        if corrida.motorista != motorista:
            return JsonResponse(
                {"success": False, "message": "Você não é o motorista desta corrida."}
            )

        # Validar transições de status
        if novo_status == CorridaStatus.EM_ANDAMENTO and corrida.pode_ser_iniciada:
            corrida.status = CorridaStatus.EM_ANDAMENTO
            corrida.data_hora_inicio = timezone.now()
            mensagem_notificacao = "Sua corrida foi iniciada!"

        elif (
            novo_status == CorridaStatus.MOTORISTA_CHEGOU
            and corrida.pode_marcar_chegada
        ):
            corrida.status = CorridaStatus.MOTORISTA_CHEGOU
            corrida.data_hora_chegada = timezone.now()
            mensagem_notificacao = "O motorista chegou ao local!"

        elif novo_status == CorridaStatus.CONCLUIDA and corrida.pode_ser_finalizada:
            corrida.status = CorridaStatus.CONCLUIDA
            corrida.data_hora_finalizacao = timezone.now()
            # Atualizar estatísticas do motorista
            motorista.total_corridas += 1
            motorista.save()
            mensagem_notificacao = "Sua corrida foi concluída!"

        else:
            return JsonResponse(
                {"success": False, "message": "Transição de status inválida."}
            )

        corrida.save()

        # Criar notificação para o paciente
        Notificacao.objects.create(
            usuario=corrida.paciente.usuario,
            tipo=(
                "corrida_iniciada"
                if novo_status == CorridaStatus.EM_ANDAMENTO
                else (
                    "motorista_chegou"
                    if novo_status == CorridaStatus.MOTORISTA_CHEGOU
                    else "corrida_finalizada"
                )
            ),
            titulo=mensagem_notificacao,
            mensagem=f"Status da corrida atualizado para: {corrida.get_status_display()}",
            corrida=corrida,
        )

        return JsonResponse(
            {
                "success": True,
                "message": "Status atualizado com sucesso!",
                "new_status": corrida.status,
                "new_status_display": corrida.get_status_display(),
            }
        )

    except Exception:
        return JsonResponse(
            {"success": False, "message": "Erro interno. Tente novamente."}
        )
