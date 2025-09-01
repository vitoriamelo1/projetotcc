from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

def index(request):
    """
    View para a página inicial do app rodas.
    """
    context = {
        'title': 'Esperança Sobre Rodas - Início',
    }
    return render(request, 'rodas/index.html', context)


def sobre(request):
    """
    View para a página sobre o projeto.
    """
    context = {
        'title': 'Sobre - Esperança Sobre Rodas',
    }
    return render(request, 'rodas/sobre.html', context)


def contato(request):
    """
    View para a página de contato.
    """
    if request.method == 'POST':
        # Processar o formulário de contato
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        
        # Aqui você pode adicionar a lógica para salvar no banco de dados
        # ou enviar por email
        
        messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
        
    context = {
        'title': 'Contato - Esperança Sobre Rodas',
    }
    return render(request, 'rodas/contato.html', context)


def login_view(request):
    """
    View para login de usuários.
    """
    if request.user.is_authenticated:
        return redirect('rodas:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'rodas:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    context = {
        'title': 'Login - Esperança Sobre Rodas',
    }
    return render(request, 'rodas/auth/login.html', context)


def logout_view(request):
    """
    View para logout de usuários.
    """
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('rodas:index')


def register_view(request):
    """
    View para registro de novos usuários.
    """
    if request.user.is_authenticated:
        return redirect('rodas:dashboard')
    
    if request.method == 'POST':
        # Implementar lógica de registro aqui
        messages.info(request, 'Funcionalidade de registro em desenvolvimento.')
    
    context = {
        'title': 'Registro - Esperança Sobre Rodas',
    }
    return render(request, 'rodas/auth/register.html', context)


def password_reset_view(request):
    """
    View para solicitar reset de senha.
    """
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='rodas/auth/password_reset_email.html',
                html_email_template_name='rodas/auth/password_reset_email.html',
                subject_template_name='rodas/auth/password_reset_subject.txt',
                from_email='noreply@esperancasobrerodas.org',
            )
            messages.success(request, 'Instruções para redefinir sua senha foram enviadas para seu email.')
            return redirect('rodas:login')
    else:
        form = PasswordResetForm()
    
    context = {
        'title': 'Esqueceu a Senha - Esperança Sobre Rodas',
        'form': form,
    }
    return render(request, 'rodas/auth/password_reset.html', context)


@login_required
def dashboard_view(request):
    """
    View do dashboard - exemplo de área restrita.
    """
    context = {
        'title': 'Dashboard - Esperança Sobre Rodas',
        'user': request.user,
    }
    return render(request, 'rodas/dashboard.html', context)


@login_required
def profile_view(request):
    """
    View do perfil do usuário - exemplo de área restrita.
    """
    context = {
        'title': 'Meu Perfil - Esperança Sobre Rodas',
        'user': request.user,
    }
    return render(request, 'rodas/profile.html', context)
