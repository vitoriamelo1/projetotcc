# 📋 Documentação dos Models - Esperança Sobre Rodas

## 🎯 Visão Geral

Este sistema implementa todos os models necessários para o funcionamento completo do aplicativo "Esperança Sobre Rodas", incluindo gerenciamento de usuários, agendamento de corridas, avaliações e notificações.

## 🏗️ Estrutura dos Models

### 1. **Usuario** (Modelo de Usuário Customizado)
- **Herança**: `AbstractUser` do Django
- **Tipos de usuário**: Paciente, Motorista, Administrador
- **Campos principais**:
  - `tipo_usuario`: Tipo do usuário (paciente/motorista/admin)
  - `telefone`: Telefone formatado (11) 99999-9999
  - `cpf`: CPF único formatado 000.000.000-00
  - `data_nascimento`: Data de nascimento
  - `endereco_completo`: Endereço completo
  - `cidade`, `estado`, `cep`: Localização
  - `ativo`: Status do usuário

### 2. **Paciente** (Perfil do Paciente)
- **Relacionamento**: OneToOne com Usuario
- **Campos específicos**:
  - `responsavel_nome`, `responsavel_cpf`, `responsavel_telefone`: Dados do responsável
  - `necessita_cadeira_rodas`: Necessidade de cadeira de rodas
  - `imunossuprimido`: Status de imunossupressão
  - `observacoes_medicas`: Observações importantes
  - `aceite_termos`: Aceite dos termos de uso
  - `data_aceite_termos`: Data do aceite

### 3. **Motorista** (Perfil do Motorista Voluntário)
- **Relacionamento**: OneToOne com Usuario
- **Status**: Pendente, Aprovado, Rejeitado, Suspenso
- **Campos específicos**:
  - `marca_veiculo`, `modelo_veiculo`, `cor_veiculo`: Dados do veículo
  - `ano_veiculo`, `placa_veiculo`: Informações complementares
  - `cnh_numero`, `cnh_validade`: Dados da CNH
  - `status_aprovacao`: Status da aprovação do cadastro
  - `online`: Status online/offline
  - `aceite_termos_voluntariado`: Aceite dos termos
  - `avaliacao_media`: Avaliação média recebida
  - `total_corridas`: Total de corridas realizadas

### 4. **Corrida** (Modelo Principal)
- **Status**: Pendente, Aceita, Em Andamento, Motorista Chegou, Concluída, Cancelada
- **Relacionamentos**: 
  - ForeignKey para Paciente (obrigatório)
  - ForeignKey para Motorista (opcional)
- **Campos principais**:
  - `endereco_origem`, `endereco_destino`: Endereços
  - `latitude_origem`, `longitude_origem`: Coordenadas origem
  - `latitude_destino`, `longitude_destino`: Coordenadas destino
  - `data_hora_agendada`: Data/hora do agendamento
  - `data_hora_aceite`, `data_hora_inicio`, `data_hora_chegada`, `data_hora_finalizacao`: Timestamps do fluxo
  - `numero_passageiros`: Quantidade de passageiros
  - `tem_acompanhante`: Se tem acompanhante
  - `necessita_cadeira_rodas`: Se precisa de cadeira de rodas
  - `observacoes`: Observações da corrida
  - `motivo_cancelamento`: Motivo se cancelada

### 5. **Avaliacao** (Sistema de Avaliações)
- **Tipos**: Paciente avalia Motorista, Motorista avalia Paciente
- **Relacionamentos**: 
  - ForeignKey para Corrida
  - ForeignKey para Usuario (avaliador)
  - ForeignKey para Usuario (avaliado)
- **Campos**:
  - `tipo_avaliacao`: Tipo da avaliação
  - `nota`: Nota de 1 a 5 estrelas
  - `comentario`: Comentário opcional
  - `data_avaliacao`: Data da avaliação

### 6. **Notificacao** (Sistema de Notificações)
- **Tipos**: Nova corrida, Corrida aceita, Motorista chegou, etc.
- **Relacionamentos**: 
  - ForeignKey para Usuario
  - ForeignKey para Corrida (opcional)
- **Campos**:
  - `tipo`: Tipo da notificação
  - `titulo`: Título da notificação
  - `mensagem`: Conteúdo da mensagem
  - `lida`: Status de leitura
  - `data_leitura`: Data da leitura

### 7. **Configuracao** (Configurações do Sistema)
- **Campos**:
  - `chave`: Chave única da configuração
  - `valor`: Valor da configuração
  - `descricao`: Descrição da configuração

## 🔄 Fluxo de Navegação Implementado

### **Login/Cadastro → Seleção de Perfil**
1. **Cadastro Paciente**:
   - Dados do responsável (nome, CPF, telefone)
   - Data de nascimento
   - Necessidades (cadeira de rodas, imunossupressão)
   - Observações médicas
   - Aceite de termos

2. **Cadastro Motorista**:
   - Dados do veículo (marca, modelo, cor)
   - Dados da CNH
   - Aceite dos termos de voluntariado
   - Status de aprovação (pendente → aprovado)

### **Paciente - Fluxo de Corrida**
1. **Agendar Corrida**:
   - Endereço de origem e destino (integração com Maps)
   - Data e hora
   - Número de passageiros
   - Necessidades especiais
   - Observações

2. **Minhas Corridas**:
   - Listagem por status
   - Informações do motorista
   - Opções: Ver detalhes, Cancelar

### **Motorista - Fluxo de Corrida**
1. **Corridas Disponíveis**:
   - Filtros (hoje, amanhã, hospital)
   - Ver detalhes
   - Aceitar corrida

2. **Detalhe da Corrida**:
   - Informações completas
   - Contato com responsável
   - Ações: Iniciar → Cheguei → Finalizar

3. **Controle de Status**:
   - Online/Offline
   - Minhas corridas aceitas

## 🔧 Funcionalidades Implementadas

### **Validações**:
- ✅ CPF formatado e único
- ✅ Telefone formatado
- ✅ CEP formatado
- ✅ CNH e placa de veículo
- ✅ Validação de campos obrigatórios

### **Relacionamentos**:
- ✅ Usuario → Paciente/Motorista (OneToOne)
- ✅ Corrida → Paciente/Motorista (ForeignKey)
- ✅ Avaliacao → Usuario/Corrida (ForeignKey)
- ✅ Notificacao → Usuario/Corrida (ForeignKey)

### **Estados e Fluxos**:
- ✅ Status de corrida com transições
- ✅ Status de aprovação de motorista
- ✅ Sistema de notificações
- ✅ Sistema de avaliações

### **Métodos Utilitários**:
- ✅ Properties para validação de estados
- ✅ Métodos para marcar notificações como lidas
- ✅ Cálculo de avaliação média
- ✅ Informações do veículo completo

## 🚀 Próximos Passos

1. **Aplicar Migrations**: `python manage.py migrate`
2. **Criar Superuser**: `python manage.py createsuperuser`
3. **Implementar Views**: Views para cada funcionalidade
4. **Templates Específicos**: Templates para cada tipo de usuário
5. **APIs**: Endpoints para mobile/frontend
6. **Integração Maps**: Google Maps API
7. **Sistema de Notificações**: Push notifications
8. **Relatórios**: Dashboard administrativo

## 📊 Estrutura do Banco de Dados

```
Usuario (AbstractUser customizado)
├── Paciente (OneToOne)
│   └── Corrida (ForeignKey)
└── Motorista (OneToOne)
    └── Corrida (ForeignKey)

Corrida
├── Avaliacao (ForeignKey)
└── Notificacao (ForeignKey)

Configuracao (standalone)
```

Os models estão prontos para suportar todo o fluxo descrito na navegação, desde o cadastro até a finalização das corridas com avaliações!
