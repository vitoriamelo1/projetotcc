# Documentação do Fluxo de Views e Templates

Este documento detalha o fluxo de requisições, a lógica de negócio contida nas `views` e como elas se conectam aos `templates` para renderizar a interface do usuário no projeto "Esperança Sobre Rodas".

## 1. Visão Geral do Padrão View-Template

O Django utiliza o padrão MVT (Model-View-Template). Neste contexto:

- **Model:** Define a estrutura dos dados (`rodas/models.py`).
- **View:** Contém a lógica que processa a requisição do usuário, interage com os models e decide qual template renderizar (`rodas/views.py`).
- **Template:** É o arquivo HTML que define a estrutura da página. Ele recebe dados da view para serem exibidos dinamicamente (`rodas/templates/rodas/**/*.html`).

## 2. Fluxo Detalhado das Views Principais

As views estão localizadas em `rodas/views.py` e são mapeadas para URLs em `rodas/urls.py`.

### 2.1. Autenticação e Cadastro

O fluxo de autenticação é central para o sistema, pois define o acesso aos diferentes perfis (Paciente e Motorista).

- **`login_view`**:

  - **Template:** `rodas/auth/login.html`
  - **Lógica:**
    1. Se o usuário já está logado, redireciona para o `dashboard`.
    2. Recebe `email` e `password` via POST.
    3. Usa a função `authenticate()` do Django para verificar as credenciais.
    4. Se válido, `login()` é chamado para iniciar a sessão e o usuário é redirecionado para o dashboard.
    5. Se inválido, uma mensagem de erro é exibida no mesmo template.

- **`register_view` (Paciente)**:

  - **Template:** `rodas/paciente/register.html`
  - **Formulário:** `PacienteRegisterForm`
  - **Lógica:**
    1. Exibe um formulário de cadastro para pacientes.
    2. Após o POST, valida os dados com `form.is_valid()`.
    3. Se válido, cria um `Usuario` com `tipo_usuario='paciente'`.
    4. Em seguida, cria um perfil `Paciente` associado a este usuário.
    5. Redireciona para a página de `login` com uma mensagem de sucesso.

- **`register_motorista_view`**:

  - **Template:** `rodas/motorista/register.html`
  - **Formulário:** `MotoristaRegisterForm`
  - **Lógica:** Similar ao registro de paciente, mas:
    1. Cria um `Usuario` com `tipo_usuario='motorista'`.
    2. Cria um perfil `Motorista` com `status_aprovacao='pendente'`.
    3. Informa ao usuário que seu cadastro passará por uma análise.

- **`logout_view`**:
  - **Lógica:** Simplesmente chama a função `logout()` do Django e redireciona para a página inicial (`index`).

### 2.2. Dashboards por Perfil

A `dashboard_view` é a principal porta de entrada após o login e age como um "roteador" com base no tipo de usuário.

- **`dashboard_view`**:
  - **Lógica:**
    1. Verifica o `request.user.tipo_usuario`.
    2. **Se Paciente:**
        - **Template:** `rodas/paciente/dashboard.html`
        - Busca o perfil `Paciente`.
        - Coleta estatísticas (total de corridas, concluídas, pendentes).
        - Renderiza o dashboard do paciente, que inclui:
          - `_solicita_corrida_form.html`: Formulário para solicitar novas corridas.
          - `_corridas_recentes.html`: Lista das últimas corridas.
    3. **Se Motorista:**
        - **Template:** `rodas/motorista/dashboard.html`
        - Busca o perfil `Motorista`.
        - Busca corridas pendentes (disponíveis para aceite).
        - Busca as corridas já aceitas pelo motorista.
        - Renderiza o dashboard do motorista, que inclui:
          - `_corridas_pendentes.html`: Lista de corridas que ele pode aceitar.
          - `_corridas_historico.html`: Suas corridas agendadas/passadas.

### 2.3. Fluxo de Gerenciamento de Corridas

Este é o fluxo mais complexo, envolvendo interações entre pacientes e motoristas, com suporte a AJAX para uma melhor experiência do usuário.

#### Lado do Paciente

- **`solicitar_corrida_view` (Endpoint POST)**:
  - **Lógica:**
    1. Recebe dados do formulário `SolicitaCorridaform` via POST.
    2. Verifica se a requisição é **AJAX** (header `X-Requested-With`).
    3. Se o formulário for válido:
        - Cria um objeto `Corrida` com status `PENDENTE`.
        - **Se AJAX:** Retorna `JsonResponse` com `success: True`.
        - **Se não AJAX:** Redireciona para o `dashboard` com uma mensagem de sucesso.
    4. Se o formulário for inválido:
        - **Se AJAX:** Retorna `JsonResponse` com `success: False` e um dicionário de `errors`, permitindo que o frontend exiba os erros nos campos corretos.
        - **Se não AJAX:** Redireciona para o `dashboard` com uma mensagem de erro.

#### Lado do Motorista

- **`aceitar_corrida_view` (Endpoint POST)**:

  - **Lógica (API-like):**
    1. Verifica se o usuário é um motorista aprovado e online.
    2. Busca a `Corrida` pelo ID.
    3. Usa a propriedade `corrida.pode_ser_aceita` para garantir que a corrida ainda está `PENDENTE`.
    4. Se tudo estiver correto:
        - Atribui o motorista à corrida.
        - Muda o status para `ACEITA`.
        - Cria uma `Notificacao` para o paciente.
        - Retorna `JsonResponse` com `success: True` e uma URL de redirecionamento.

- **`atualizar_status_corrida_view` (Endpoint POST)**:
  - **Lógica (API-like):**
    1. Recebe o `novo_status` do corpo da requisição JSON.
    2. Verifica se o motorista logado é o motorista da corrida.
    3. Usa as propriedades do modelo `Corrida` (`pode_ser_iniciada`, `pode_marcar_chegada`, etc.) para validar a transição de estado.
    4. Se a transição for válida:
        - Atualiza o status da corrida e o timestamp correspondente (ex: `data_hora_inicio`).
        - Cria uma `Notificacao` para o paciente.
        - Retorna `JsonResponse` com o novo status.
    5. Se inválida, retorna um erro.

### 2.4. Visualização de Detalhes e Listas

- **`corrida_detalhes_view`**:

  - **Templates:** `rodas/paciente/corrida_detalhes.html` e `rodas/motorista/corrida_detalhes.html`
  - **Lógica:**
    1. Busca a `Corrida` pelo ID.
    2. Implementa uma lógica de permissão rigorosa:
        - Pacientes só podem ver suas próprias corridas.
        - Motoristas só podem ver corridas `PENDENTES` ou aquelas que eles aceitaram.
    3. Renderiza o template de detalhes apropriado para o tipo de usuário.

- **`corridas_paciente_list_view` / `corridas_motorista_list_view`**:
  - **Templates:** `rodas/paciente/corridas_list.html` e `rodas/motorista/corridas_list.html`
  - **Lógica:**
    1. Lista todas as corridas associadas ao usuário.
    2. Permite filtrar por `status` através de um parâmetro GET (`?status=concluida`).
    3. Utiliza o `Paginator` do Django para dividir os resultados em várias páginas.

## 3. Estrutura e Reutilização de Templates

A pasta `rodas/templates/rodas/` é organizada para maximizar a reutilização de código:

- **`base.html`**: O template principal que define a estrutura de todas as páginas (cabeçalho, rodapé, inclusão de CSS/JS). Outros templates estendem este usando `{% extends 'rodas/base.html' %}`.
- **Pastas por Perfil (`paciente/`, `motorista/`)**: Contêm templates específicos para cada tipo de usuário, como seus dashboards e formulários de cadastro.
- **Templates Parciais (prefixo `_`)**: Arquivos como `_corridas_recentes.html` são fragmentos de HTML incluídos em templates maiores (como o `dashboard.html`) usando a tag `{% include %}`. Isso evita a repetição de código e organiza melhor a interface.
- **Pasta `auth/`**: Contém todos os templates relacionados ao fluxo de autenticação (login, reset de senha, etc.), mantendo-os organizados.

Este design modular de views e templates permite um desenvolvimento organizado, seguro e escalável, onde cada componente tem uma responsabilidade clara.
