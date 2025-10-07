from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone
from decimal import Decimal
from typing import Any


class UserManager(BaseUserManager):
    """
    Gerenciador customizado para o modelo de usuário
    """

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields: Any) -> "Usuario":
        """
        Cria e salva um usuário com o email e senha fornecidos
        """
        if not email:
            raise ValueError("O email deve ser fornecido")
        email = self.normalize_email(email)
        user: Usuario = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str = None, **extra_fields: Any
    ) -> "Usuario":
        """
        Cria e salva um usuário regular
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **extra_fields: Any
    ) -> "Usuario":
        """
        Cria e salva um superusuário
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("tipo_usuario", TipoUsuario.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário deve ter is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AbstractUsuario(AbstractBaseUser, PermissionsMixin):
    """
    Classe abstrata para o modelo de usuário customizado
    """

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Endereço de email único para login",
    )
    nome_completo = models.CharField(max_length=150, verbose_name="Nome Completo")
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Membro da Equipe",
        help_text="Designa se o usuário pode acessar o site de administração.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Designa se este usuário deve ser tratado como ativo. Desmarque esta opção ao invés de deletar contas.",
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True, verbose_name="Última Atualização"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome_completo"]

    class Meta:
        abstract = True
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self) -> str:
        return self.get_full_name() or self.email

    def get_full_name(self) -> str:
        """
        Retorna o nome completo do usuário
        """
        return self.nome_completo

    def get_short_name(self) -> str:
        """
        Retorna o primeiro nome do usuário
        """
        return (
            self.nome_completo.split(" ")[0]
            if self.nome_completo
            else self.email.split("@")[0]
        )

    def email_user(
        self, subject: str, message: str, from_email: str = None, **kwargs: Any
    ) -> None:
        """
        Envia um email para este usuário
        """
        from django.core.mail import send_mail

        send_mail(subject, message, from_email, [self.email], **kwargs)


class TipoUsuario(models.TextChoices):
    PACIENTE = "paciente", "Paciente"
    MOTORISTA = "motorista", "Motorista Voluntário"
    ADMIN = "admin", "Administrador"


class Usuario(AbstractUsuario):
    """
    Modelo de usuário customizado que estende o User padrão do Django
    """

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default="paciente",
        verbose_name="Tipo de Usuário",
    )
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\(\d{2}\)\s\d{4,5}-\d{4}$")],
        verbose_name="Telefone",
        help_text="Formato: (11) 99999-9999",
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
        verbose_name="CPF",
        help_text="Formato: 000.000.000-00",
    )
    data_nascimento = models.DateField(
        null=True, blank=True, verbose_name="Data de Nascimento"
    )
    endereco_completo = models.TextField(blank=True, verbose_name="Endereço Completo")
    cidade = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, verbose_name="Estado")
    cep = models.CharField(
        max_length=9,
        blank=True,
        validators=[RegexValidator(r"^\d{5}-\d{3}$")],
        verbose_name="CEP",
        help_text="Formato: 00000-000",
    )
    ativo = models.BooleanField(default=True, verbose_name="Usuário Ativo")
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True, verbose_name="Última Atualização"
    )

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        nome = self.get_full_name() or self.username
        for valor, display in TipoUsuario.choices:
            if valor == self.tipo_usuario:
                return f"{nome} ({display})"
        return nome


class Paciente(models.Model):
    """
    Perfil específico para pacientes
    """

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_paciente"
    )
    responsavel_nome = models.CharField(
        max_length=200, verbose_name="Nome do Responsável"
    )
    responsavel_cpf = models.CharField(
        max_length=14,
        validators=[RegexValidator(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")],
        verbose_name="CPF do Responsável",
    )
    responsavel_telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\(\d{2}\)\s\d{4,5}-\d{4}$")],
        verbose_name="Telefone do Responsável",
    )
    necessita_cadeira_rodas = models.BooleanField(
        default=False, verbose_name="Necessita Cadeira de Rodas"
    )
    imunossuprimido = models.BooleanField(
        default=False, verbose_name="Paciente Imunossuprimido"
    )
    observacoes_medicas = models.TextField(
        blank=True,
        verbose_name="Observações Médicas",
        help_text="Informações importantes sobre necessidades especiais",
    )
    aceite_termos = models.BooleanField(
        default=False, verbose_name="Aceite dos Termos de Uso"
    )
    data_aceite_termos = models.DateTimeField(
        null=True, blank=True, verbose_name="Data do Aceite dos Termos"
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self) -> str:
        return f"Paciente: {self.usuario.get_full_name() or self.usuario.username}"


class Motorista(models.Model):
    """
    Perfil específico para motoristas voluntários
    """

    STATUS_CHOICES = [
        ("pendente", "Cadastro em Análise"),
        ("aprovado", "Aprovado"),
        ("rejeitado", "Rejeitado"),
        ("suspenso", "Suspenso"),
    ]

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_motorista"
    )
    marca_veiculo = models.CharField(max_length=50, verbose_name="Marca do Veículo")
    modelo_veiculo = models.CharField(max_length=50, verbose_name="Modelo do Veículo")
    cor_veiculo = models.CharField(max_length=30, verbose_name="Cor do Veículo")
    ano_veiculo = models.IntegerField(
        null=True, blank=True, verbose_name="Ano do Veículo"
    )
    placa_veiculo = models.CharField(
        max_length=8,
        blank=True,
        validators=[RegexValidator(r"^[A-Z]{3}-?\d{4}|[A-Z]{3}\d[A-Z]\d{2}$")],
        verbose_name="Placa do Veículo",
        help_text="Formato: ABC-1234 ou ABC1D23",
    )
    cnh_numero = models.CharField(
        max_length=20, blank=True, verbose_name="Número da CNH"
    )
    cnh_validade = models.DateField(
        null=True, blank=True, verbose_name="Validade da CNH"
    )
    status_aprovacao = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendente",
        verbose_name="Status da Aprovação",
    )
    online = models.BooleanField(default=False, verbose_name="Motorista Online")
    aceite_termos_voluntariado = models.BooleanField(
        default=False, verbose_name="Aceite dos Termos de Voluntariado"
    )
    data_aceite_termos = models.DateTimeField(
        null=True, blank=True, verbose_name="Data do Aceite dos Termos"
    )
    avaliacao_media = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Avaliação Média",
    )
    total_corridas = models.IntegerField(
        default=0, verbose_name="Total de Corridas Realizadas"
    )
    data_aprovacao = models.DateTimeField(
        null=True, blank=True, verbose_name="Data da Aprovação"
    )
    observacoes_admin = models.TextField(
        blank=True, verbose_name="Observações da Administração"
    )

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"

    def __str__(self) -> str:
        nome = self.usuario.get_full_name() or self.usuario.username
        for valor, display in self.STATUS_CHOICES:
            if valor == self.status_aprovacao:
                return f"Motorista: {nome} - {display}"
        return f"Motorista: {nome}"

    @property
    def veiculo_completo(self) -> str:
        return f"{self.marca_veiculo} {self.modelo_veiculo} {self.cor_veiculo}"


class CorridaStatus(models.TextChoices):
    PENDENTE = "pendente", "Pendente"
    ACEITA = "aceita", "Aceita"
    EM_ANDAMENTO = "em_andamento", "Em Andamento"
    MOTORISTA_CHEGOU = "motorista_chegou", "Motorista Chegou"
    CONCLUIDA = "concluida", "Concluída"
    CANCELADA = "cancelada", "Cancelada"


class Corrida(models.Model):
    """
    Modelo principal para as corridas/viagens
    """

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="corridas",
        verbose_name="Paciente",
    )
    motorista = models.ForeignKey(
        Motorista,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="corridas",
        verbose_name="Motorista",
    )

    # Endereços
    endereco_origem = models.TextField(verbose_name="Endereço de Origem")
    latitude_origem = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name="Latitude Origem",
    )
    longitude_origem = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name="Longitude Origem",
    )

    endereco_destino = models.TextField(verbose_name="Endereço de Destino")
    latitude_destino = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name="Latitude Destino",
    )
    longitude_destino = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name="Longitude Destino",
    )

    # Data e hora
    data_hora_agendada = models.DateTimeField(verbose_name="Data e Hora Agendada")
    data_hora_aceite = models.DateTimeField(
        null=True, blank=True, verbose_name="Data e Hora do Aceite"
    )
    data_hora_inicio = models.DateTimeField(
        null=True, blank=True, verbose_name="Data e Hora do Início"
    )
    data_hora_chegada = models.DateTimeField(
        null=True, blank=True, verbose_name="Data e Hora da Chegada"
    )
    data_hora_finalizacao = models.DateTimeField(
        null=True, blank=True, verbose_name="Data e Hora da Finalização"
    )

    # Detalhes da corrida
    numero_passageiros = models.IntegerField(
        default=1, verbose_name="Número de Passageiros"
    )
    tem_acompanhante = models.BooleanField(
        default=False, verbose_name="Tem Acompanhante"
    )
    necessita_cadeira_rodas = models.BooleanField(
        default=False, verbose_name="Necessita Cadeira de Rodas"
    )
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    # Status e controle
    status = models.CharField(
        max_length=20,
        choices=CorridaStatus.choices,
        default=CorridaStatus.PENDENTE,
        verbose_name="Status",
    )

    # Dados de criação e atualização
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True, verbose_name="Última Atualização"
    )

    # Motivo de cancelamento
    motivo_cancelamento = models.TextField(
        blank=True, null=True, verbose_name="Motivo do Cancelamento"
    )
    data_cancelamento = models.DateTimeField(
        null=True, blank=True, verbose_name="Data do Cancelamento"
    )
    cancelada_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="corridas_canceladas",
        verbose_name="Cancelada Por",
    )

    class Meta:
        verbose_name = "Corrida"
        verbose_name_plural = "Corridas"
        ordering = ["-data_criacao"]

    def __str__(self) -> str:
        paciente_nome = (
            self.paciente.usuario.get_full_name() or self.paciente.usuario.username
        )
        for valor, display in CorridaStatus.choices:
            if valor == self.status:
                return f"Corrida #{self.pk} - {paciente_nome} - {display}"
        return f"Corrida #{self.pk} - {paciente_nome}"

    @property
    def pode_ser_aceita(self) -> bool:
        return self.status == CorridaStatus.PENDENTE and self.motorista is None

    @property
    def pode_ser_iniciada(self) -> bool:
        return self.status == CorridaStatus.ACEITA and self.motorista is not None

    @property
    def pode_marcar_chegada(self) -> bool:
        return self.status == CorridaStatus.EM_ANDAMENTO

    @property
    def pode_ser_finalizada(self) -> bool:
        return self.status == CorridaStatus.MOTORISTA_CHEGOU


class Avaliacao(models.Model):
    """
    Sistema de avaliação pós-corrida
    """

    TIPO_CHOICES = [
        ("paciente_avalia_motorista", "Paciente Avalia Motorista"),
        ("motorista_avalia_paciente", "Motorista Avalia Paciente"),
    ]

    corrida = models.ForeignKey(
        Corrida,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
        verbose_name="Corrida",
    )
    avaliador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="avaliacoes_feitas",
        verbose_name="Avaliador",
    )
    avaliado = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="avaliacoes_recebidas",
        verbose_name="Avaliado",
    )
    tipo_avaliacao = models.CharField(
        max_length=30, choices=TIPO_CHOICES, verbose_name="Tipo de Avaliação"
    )
    nota = models.IntegerField(
        choices=[(i, f"{i} estrela{'s' if i > 1 else ''}") for i in range(1, 6)],
        verbose_name="Nota (1-5 estrelas)",
    )
    comentario = models.TextField(blank=True, verbose_name="Comentário")
    data_avaliacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data da Avaliação"
    )

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ["corrida", "avaliador", "tipo_avaliacao"]

    def __str__(self) -> str:
        for valor, display in self.TIPO_CHOICES:
            if valor == self.tipo_avaliacao:
                return f"Avaliação: {self.nota} estrelas - {display}"
        return f"Avaliação: {self.nota} estrelas"


class Notificacao(models.Model):
    """
    Sistema de notificações para usuários
    """

    TIPO_CHOICES = [
        ("nova_corrida", "Nova Corrida Disponível"),
        ("corrida_aceita", "Corrida Aceita"),
        ("corrida_iniciada", "Corrida Iniciada"),
        ("motorista_chegou", "Motorista Chegou"),
        ("corrida_finalizada", "Corrida Finalizada"),
        ("corrida_cancelada", "Corrida Cancelada"),
        ("avaliacao_recebida", "Avaliação Recebida"),
        ("aprovacao_motorista", "Aprovação de Motorista"),
        ("sistema", "Notificação do Sistema"),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="notificacoes",
        verbose_name="Usuário",
    )
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, verbose_name="Tipo")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensagem = models.TextField(verbose_name="Mensagem")
    corrida = models.ForeignKey(
        Corrida,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notificacoes",
        verbose_name="Corrida Relacionada",
    )
    lida = models.BooleanField(default=False, verbose_name="Lida")
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Criação"
    )
    data_leitura = models.DateTimeField(
        null=True, blank=True, verbose_name="Data da Leitura"
    )

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ["-data_criacao"]

    def __str__(self) -> str:
        usuario_nome = self.usuario.get_full_name() or self.usuario.username
        return f"Notificação: {self.titulo} - {usuario_nome}"

    def marcar_como_lida(self) -> None:
        if not self.lida:
            self.lida = True
            self.data_leitura = timezone.now()
            self.save(update_fields=["lida", "data_leitura"])


class Configuracao(models.Model):
    """
    Configurações gerais do sistema
    """

    chave = models.CharField(max_length=100, unique=True, verbose_name="Chave")
    valor = models.TextField(verbose_name="Valor")
    descricao = models.CharField(max_length=200, blank=True, verbose_name="Descrição")
    data_atualizacao = models.DateTimeField(
        auto_now=True, verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Configuração"
        verbose_name_plural = "Configurações"

    def __str__(self) -> str:
        valor_str = str(self.valor)
        if len(valor_str) > 50:
            return f"{self.chave}: {valor_str[:50]}..."
        return f"{self.chave}: {valor_str}"
