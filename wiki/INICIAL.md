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

- Docker e Docker Compose

## 🛠️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd esperanca-sobre-rodas
```

### 2. Configure as variáveis de ambiente

Copie o arquivo de exemplo `.env.example` para `.env`:

```bash
cp .env.example .env
```

#### Explicação dos campos do `.env.example`:

- **DB_NAME**: Nome do banco de dados PostgreSQL.
- **DB_USER**: Usuário do banco de dados.
- **DB_PASS**: Senha do banco de dados.
- **DB_HOST**: Host do banco de dados (normalmente `localhost` ou o nome do serviço no Docker).
- **DB_PORT**: Porta do banco de dados (padrão PostgreSQL é 5432, mas pode variar).
- **DJANGO_ALLOWED_HOSTS**: Lista de hosts permitidos para acesso à aplicação Django.
- **DJANGO_SECRET_KEY**: Chave secreta usada pelo Django para segurança.
- **DJANGO_LOG_LEVEL**: Nível de log do Django (`DEBUG`, `INFO`, etc).
- **EMAIL_HOST**: Host do servidor de e-mail.
- **EMAIL_PORT**: Porta do servidor de e-mail.
- **EMAIL_HOST_USER**: Usuário do servidor de e-mail.
- **EMAIL_HOST_PASSWORD**: Senha do servidor de e-mail.
- **DEFAULT_FROM_EMAIL**: E-mail padrão para envio.
- **REDIS_URL**: URL de conexão com o Redis (usado para cache ou fila de tarefas).

### 3. Inicie o projeto com Docker Compose

Certifique-se de que o Docker e o Docker Compose estão instalados. Para subir os serviços (banco de dados, Redis, etc):

```bash
docker compose --profile app up app
```

Para rodar em modo de produção, utilize:

```bash
docker compose -f docker-compose.prod.yml up
```

Isso irá iniciar todos os serviços definidos nos arquivos de configuração. O Django pode ser acessado pelo endereço definido em `DJANGO_ALLOWED_HOSTS`.
