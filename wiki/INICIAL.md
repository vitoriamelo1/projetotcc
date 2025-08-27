# Esperança Sobre Rodas

Um projeto Django para gerenciar uma iniciativa social voltada ao transporte.

## 🚀 Tecnologias Utilizadas

### Backend
- **Django 5.2.5** - Framework web principal
- **Python 3.12+** - Linguagem de programação
- **PostgreSQL 17** - Banco de dados relacional
- **psycopg2-binary** - Adaptador PostgreSQL para Python
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Infraestrutura
- **Docker & Docker Compose** - Containerização do banco de dados
- **uv** - Gerenciador de dependências Python moderno

## 📋 Pré-requisitos

- Python 3.12 ou superior
- Docker e Docker Compose
- uv (gerenciador de dependências)

## 🛠️ Configuração do Ambiente

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd esperanca-sobre-rodas
```

### 2. Configuração do ambiente virtual e dependências
```bash
# Instalar dependências com uv
uv sync

# Ativar ambiente virtual
source .venv/bin/activate
```

### 3. Configuração do banco de dados
```bash
# Iniciar o PostgreSQL com Docker
docker-compose up -d
```

### 4. Configuração das variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do banco de dados
DB_NAME=rodas
DB_USER=rodas
DB_PASSWORD=rodas
DB_HOST=localhost
DB_PORT=5439

# Configurações do Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
```

## 🚀 Inicializando a Aplicação

### 1. Aplicar migrações do banco de dados
```bash
python manage.py migrate
```

### 2. Criar superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 3. Executar o servidor de desenvolvimento
```bash
python manage.py runserver
```

A aplicação estará disponível em: http://127.0.0.1:8000

## 📚 Comandos Úteis do Django

### Gerenciamento do Banco de Dados
```bash
# Criar migrações após alterações nos models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Reverter migração específica
python manage.py migrate app_name migration_name

# Mostrar status das migrações
python manage.py showmigrations
```

### Gerenciamento de Aplicações
```bash
# Criar nova aplicação Django
python manage.py startapp nome_da_app

# Verificar configuração do projeto
python manage.py check
```

### Utilitários
```bash
# Abrir shell interativo do Django
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test

# Limpar cache
python manage.py clear_cache
```

### Dados e Fixtures
```bash
# Exportar dados para fixture
python manage.py dumpdata app_name > fixture_name.json

# Carregar dados de fixture
python manage.py loaddata fixture_name.json

# Flush do banco (limpar todos os dados)
python manage.py flush
```

## 🗄️ Estrutura do Banco de Dados

O projeto utiliza PostgreSQL com as seguintes configurações:
- **Host**: localhost
- **Porta**: 5439
- **Database**: rodas
- **Usuário**: rodas
- **Senha**: rodas

## 🔧 Desenvolvimento

### Instalação de novas dependências
```bash
# Adicionar nova dependência
uv add nome-do-pacote

# Adicionar dependência de desenvolvimento
uv add --dev nome-do-pacote

# Remover dependência
uv remove nome-do-pacote
```

### Comandos Docker
```bash
# Iniciar apenas o banco de dados
docker-compose up db

# Parar os serviços
docker-compose down

# Ver logs do banco
docker-compose logs db

# Reconstruir containers
docker-compose build
```

## 📁 Estrutura do Projeto

```
esperanca-sobre-rodas/
├── core/                 # Configurações principais do Django
│   ├── __init__.py
│   ├── settings.py      # Configurações do projeto
│   ├── urls.py          # URLs principais
│   ├── wsgi.py          # Configuração WSGI
│   └── asgi.py          # Configuração ASGI
├── manage.py            # Script de gerenciamento Django
├── pyproject.toml       # Dependências e configurações do projeto
├── uv.lock             # Lock file das dependências
├── docker-compose.yml   # Configuração do Docker
└── README.md           # Documentação
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença [especificar licença].

## 📞 Contato

Para mais informações sobre o projeto, entre em contato com a equipe de desenvolvimento.
