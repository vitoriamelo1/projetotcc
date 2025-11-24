# Esperança Sobre Rodas

Com a implementação do sistema "Esperança sobre Rodas", espera-se proporcionar ummeio de transporte seguro, gratuito e eficiente para crianças e adolescentes em tratamento oncológico.

A disponibilidade desse serviço pretende reduzir significativamente o número de faltas às sessões de quimioterapia e radioterapia, fortalecendo a continuidade terapêutica e melhorando as chances de sucesso clínico.

O aplicativo deverá otimizar a logística de transporte ao conectar pacientes a motoristas voluntários disponíveis de forma ágil e inteligente, minimizando tempos de espera e garantindo maior eficiência no atendimento. Além disso, o sistema será desenvolvido com foco em alta segurança da informação, assegurando a privacidade e a proteção dos dados sensíveis dos usuários, o que deverá aumentar a confiança e a adesão à plataforma.

Outro resultado esperado é a criação de uma experiência de usuário intuitiva e amigável, capaz de incentivar tanto os pacientes quanto os motoristas a utilizarem a ferramenta de maneira constante.

Com a consolidação da rede de voluntariado, pretende-se mobilizar ativamente a sociedade civil, fortalecendo laços comunitários e promovendo a solidariedade social.
Espera-se também que o sistema contribua para ampliar a capacidade de atendimento dos hospitais, ao possibilitar que mais pacientes completem seus tratamentos sem interrupções.

A coleta de dados de uso da plataforma poderá oferecer informações relevantes para futuras melhorias no serviço, além de servir de subsídio para o desenvolvimento de políticas públicas voltadas ao suporte de pacientes oncológicos.

Finalmente, ao reduzir os índices de abandono terapêutico e as complicações médicas associadas, o projeto poderá ajudar a diminuir os custos indiretos do sistema público de saúde.

## Integrantes

- Ana Julia Dias Barreto - 2212188
- Breno Cappelle de Almeida - 2221510
- Maria Vitoria Matos Costa Beber - 2211107
- Vitoria Oliveira Gomes Melo - 2210249

> Projeto já finalizado no ciclo 2, no momento estamos trabalhando no desenvolviemnto da apresentação do TCC, envolvendo slide e documentação.

## Objetivos

- Facilitar o acesso de pacientes ao tratamento oncológico.
- Criar uma rede de motoristas voluntários e doadores;
- Garantir a privacidade e segurança dos dados dos usuários;
- Desenvolver uma plataforma amigável e responsiva;
- Reduzir riscos de infecções por neutropenia;
- Evitar interrupção de tratamentos;
- Promover o engajamento comunitário em causas humanitárias.

## Telas do Projeto

- Home com informações iniciais;
- Tela de login;
- Tela de cadastro de usuários;
- Cadastro e agendamento de corridas;
- Vizualização e acompanhamento de corridas agendadas;
- Dashboard do motorista contendo as corridas disponíveis e concluídas;
  
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
git clone https://github.com/vitoriamelo1/projetotcc.git esperanca-sobre-rodas
cd esperanca-sobre-rodas
```

### 2. Configure as variáveis de ambiente

Copie o arquivo de exemplo `.env.example` para `.env`:

```bash
cp .env.example .env
```

#### Explicação dos campos do `.env.example`

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

### 4. Acesse a aplicação

Após iniciar os serviços, você pode acessar a aplicação Django através do navegador, utilizando o endereço configurado em `DJANGO_ALLOWED_HOSTS`. Normalmente, isso será algo como `http://localhost:8000` ou o domínio que você tenha configurado.

### 5. Parar os serviços

Para parar os serviços em execução, utilize o comando:

Modo desenvolvimento:

```bash
docker compose down
```

Modo produção:

```bash
docker compose -f docker-compose.prod.yml down
```
