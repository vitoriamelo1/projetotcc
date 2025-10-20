# Documentação do Projeto: Esperança Sobre Rodas

## 1. Introdução

O "Esperança Sobre Rodas" é uma aplicação web desenvolvida para conectar pacientes que necessitam de transporte para tratamento médico a motoristas voluntários. O sistema visa facilitar o agendamento e a gestão de corridas, oferecendo uma plataforma centralizada para pacientes, motoristas e administradores.

Este documento serve como um guia técnico detalhado sobre a arquitetura, estrutura, tecnologias e práticas de desenvolvimento adotadas no projeto. O objetivo é fornecer um entendimento claro para os membros da equipe e para a banca avaliadora do TCC.

## 2. Arquitetura do Projeto

A aplicação é construída sobre o framework **Django**, seguindo uma arquitetura Monolítica com uma única aplicação principal (`rodas`), o que simplifica o desenvolvimento e a manutenção para o escopo do projeto.

### 2.1. Componentes Principais

- **Projeto Django (`core`):** Contém as configurações globais do projeto, roteamento principal (URLs) e o ponto de entrada para o servidor web (WSGI/ASGI). As configurações são divididas em ambientes (`development`, `production`) para garantir segurança e praticidade.
- **Aplicação Django (`rodas`):** É o coração do sistema. Concentra todos os modelos de dados, views (lógica de negócio), formulários, templates (HTML) e URLs específicas da funcionalidade de corridas e usuários.
- **Banco de Dados (PostgreSQL):** Um banco de dados relacional robusto, escolhido por sua confiabilidade, escalabilidade e recursos avançados.
- **Servidor de Aplicação (Gunicorn):** Utilizado em produção para servir a aplicação Django de forma eficiente e segura.
- **Servidor de Arquivos Estáticos (WhiteNoise):** Integra-se ao Django para servir arquivos estáticos (CSS, JS, imagens) diretamente da aplicação, simplificando o deploy.
- **Frontend (TailwindCSS):** Um framework CSS "utility-first" que permite a construção de interfaces modernas e responsivas diretamente no HTML, sem a necessidade de escrever CSS customizado extensivamente.

### 2.2. Fluxo de Dados

1.  **Requisição do Usuário:** O navegador do usuário envia uma requisição HTTP para o servidor.
2.  **Roteamento Django:** O `core/urls.py` direciona a requisição para a URL correspondente na aplicação `rodas/urls.py`.
3.  **View:** A view apropriada em `rodas/views.py` é executada. Ela processa a lógica de negócio, interagindo com os modelos (`rodas/models.py`) para acessar ou modificar dados no PostgreSQL.
4.  **Renderização do Template:** A view renderiza um template HTML (`rodas/templates/rodas/`), passando os dados necessários. O TailwindCSS é aplicado para estilização.
5.  **Resposta:** O servidor envia a resposta HTML renderizada de volta ao navegador do usuário.

Para interações dinâmicas (como aceitar uma corrida), o frontend utiliza **AJAX** para enviar requisições a endpoints de API específicos, que retornam dados em formato **JSON**, permitindo a atualização da página sem recarregamento.

## 3. Estrutura de Pastas

```
/
├── core/               # Configurações do projeto Django
│   ├── settings/       # Módulos de configuração (base, dev, prod)
│   └── urls.py         # URLs globais
├── rodas/              # Aplicação principal do projeto
│   ├── migrations/     # Migrações do banco de dados
│   ├── templates/      # Arquivos HTML
│   ├── admin.py        # Configuração do painel de admin
│   ├── forms.py        # Formulários Django
│   ├── models.py       # Modelos de dados (tabelas do BD)
│   ├── urls.py         # URLs da aplicação 'rodas'
│   └── views.py        # Lógica de negócio (controllers)
├── static/             # Arquivos estáticos em desenvolvimento (CSS, JS, img)
├── staticfiles/        # Arquivos estáticos coletados para produção (gerado)
├── documentos/         # Documentação do projeto
├── manage.py           # Script de gerenciamento do Django
├── pyproject.toml      # Dependências Python (uv)
└── package.json        # Dependências JavaScript (TailwindCSS)
```

- **`core/`**: Pasta do projeto Django. Gerencia as configurações e URLs de nível superior.
- **`rodas/`**: Aplicação Django que contém a lógica principal. Segue a estrutura padrão de uma app Django.
- **`static/`**: Onde os desenvolvedores colocam os arquivos CSS, JavaScript e imagens. O `_style.css` é o arquivo fonte para o TailwindCSS.
- **`staticfiles/`**: Gerado pelo comando `collectstatic`. Contém todos os arquivos estáticos que serão servidos em produção. **Não deve ser editado manualmente.**
- **`documentos/`**: Contém a documentação funcional e técnica do projeto.

## 4. Boas Práticas e Padrões

- **Ambientes de Configuração:** O uso de `core/settings/development.py` e `core/settings/production.py` permite separar configurações sensíveis (como chaves de API e segredos) do código-fonte, utilizando variáveis de ambiente (`.env`), o que é uma prática de segurança fundamental.
- **Modelo de Usuário Customizado:** Foi criado um `Usuario` customizado (`AUTH_USER_MODEL`) para permitir login com email em vez de nome de usuário e para adicionar campos específicos como `tipo_usuario` (Paciente, Motorista, Admin).
- **Separação de Perfis:** Os modelos `Paciente` and `Motorista` são separados do `Usuario` através de uma relação `OneToOneField`. Isso mantém o modelo de autenticação limpo e organiza melhor os dados específicos de cada tipo de perfil.
- **Máquina de Estados para Corridas:** O modelo `Corrida` possui um campo `status` e propriedades (`pode_ser_aceita`, `pode_ser_iniciada`, etc.) que funcionam como "guardas" (guards). Isso garante que as transições de status ocorram apenas na ordem correta, prevenindo inconsistências nos dados.
- **Requisições AJAX com Fallback:** As views, como a `solicitar_corrida_view`, detectam se a requisição é AJAX (`X-Requested-With: XMLHttpRequest`). Se for, retornam JSON. Caso contrário, fazem um redirecionamento padrão. Isso garante que o formulário funcione mesmo que o JavaScript esteja desabilitado.
- **Gerenciamento de Dependências:** O projeto utiliza `uv` para as dependências Python e `npm` para as de frontend, o que facilita a instalação e a reprodutibilidade do ambiente de desenvolvimento.

## 5. Tecnologias Utilizadas

| Tecnologia      | Categoria                 | Justificativa                                                                                                                                          |
| :-------------- | :------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Python**      | Linguagem (Backend)       | Uma linguagem de alto nível, com sintaxe clara e um ecossistema robusto, ideal para desenvolvimento web rápido e seguro.                               |
| **Django**      | Framework (Backend)       | Framework "baterias inclusas" que oferece ORM, sistema de autenticação, painel de admin e segurança por padrão, acelerando o desenvolvimento.          |
| **PostgreSQL**  | Banco de Dados            | Um sistema de gerenciamento de banco de dados relacional de código aberto, conhecido por sua robustez, confiabilidade e conformidade com o padrão SQL. |
| **Gunicorn**    | Servidor de Aplicação     | Servidor WSGI padrão de mercado para deploy de aplicações Python em produção, garantindo performance e estabilidade.                                   |
| **WhiteNoise**  | Servidor de Estáticos     | Simplifica o deploy de arquivos estáticos em ambientes de produção sem a necessidade de configurar um servidor web complexo como o Nginx.              |
| **HTML5/CSS3**  | Linguagem (Frontend)      | Padrões fundamentais para a estruturação e estilização de páginas web.                                                                                 |
| **JavaScript**  | Linguagem (Frontend)      | Utilizado para adicionar interatividade ao cliente, como no envio de formulários via AJAX e na atualização dinâmica de componentes.                    |
| **TailwindCSS** | Framework (Frontend)      | Permite criar designs customizados de forma rápida e eficiente, escrevendo classes de utilidade diretamente no HTML, o que aumenta a produtividade.    |
| **Flowbite**    | Biblioteca de Componentes | Baseada em TailwindCSS, oferece componentes de UI prontos (modais, tooltips, etc.), acelerando o desenvolvimento da interface.                         |
| **Docker**      | Conteinerização           | Permite empacotar a aplicação e suas dependências em contêineres, garantindo que o ambiente de desenvolvimento seja idêntico ao de produção.           |
| **uv**          | Gerenciador de Pacotes    | Um gerenciador de pacotes e ambientes virtuais para Python, extremamente rápido e moderno, que substitui `pip` e `venv`.                               |
| **npm**         | Gerenciador de Pacotes    | Gerenciador de pacotes do ecossistema Node.js, utilizado para instalar e gerenciar o TailwindCSS e outras ferramentas de frontend.                     |
