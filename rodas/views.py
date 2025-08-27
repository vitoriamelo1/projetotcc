from django.shortcuts import render
from django.contrib import messages

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
