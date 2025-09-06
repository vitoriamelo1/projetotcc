from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Paciente, Motorista, Corrida, Avaliacao, Notificacao, Configuracao


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Usuario customizado
    """
    # list_display = ('get_full_name', 'email', 'tipo_usuario', 'ativo', 'data_criacao')
    # list_filter = ('tipo_usuario', 'ativo', 'is_staff', 'is_superuser', 'data_criacao')
    # search_fields = ('nome_completo', 'email', 'cpf', 'tipo')
    # ordering = ('-data_criacao',)
    #
    # fieldsets = UserAdmin.fieldsets + (
    #     ('Informações Adicionais', {
    #         'fields': ('tipo_usuario', 'telefone', 'cpf', 'data_nascimento',
    #                    'endereco_completo', 'cidade', 'estado', 'cep', 'ativo')
    #     }),
    # )
    #
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     ('Informações Adicionais', {
    #         'fields': ('tipo_usuario', 'telefone', 'cpf', 'data_nascimento')
    #     }),
    # )
    pass


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Paciente
    """
    list_display = ('get_nome_usuario', 'responsavel_nome', 'necessita_cadeira_rodas',
                    'imunossuprimido', 'aceite_termos')
    list_filter = ('necessita_cadeira_rodas', 'imunossuprimido', 'aceite_termos')
    search_fields = ('usuario__nome_completo', 'responsavel_nome',
                     'responsavel_cpf')
    readonly_fields = ('data_aceite_termos',)

    fieldsets = (
        ('Usuário', {
            'fields': ('usuario',)
        }),
        ('Dados do Responsável', {
            'fields': ('responsavel_nome', 'responsavel_cpf', 'responsavel_telefone')
        }),
        ('Informações Médicas', {
            'fields': ('necessita_cadeira_rodas', 'imunossuprimido', 'observacoes_medicas')
        }),
        ('Termos e Condições', {
            'fields': ('aceite_termos', 'data_aceite_termos')
        }),
    )

    def get_nome_usuario(self, obj):
        return obj.usuario.get_full_name()

    get_nome_usuario.short_description = 'Nome do Usuário'


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Motorista
    """
    list_display = ('get_nome_usuario', 'veiculo_completo', 'status_aprovacao',
                    'online', 'total_corridas', 'avaliacao_media')
    list_filter = ('status_aprovacao', 'online', 'aceite_termos_voluntariado')
    search_fields = ('usuario__nome_completo', 'marca_veiculo',
                     'modelo_veiculo', 'placa_veiculo')
    readonly_fields = ('data_aceite_termos', 'data_aprovacao', 'avaliacao_media', 'total_corridas')

    fieldsets = (
        ('Usuário', {
            'fields': ('usuario',)
        }),
        ('Dados do Veículo', {
            'fields': ('marca_veiculo', 'modelo_veiculo', 'cor_veiculo', 'ano_veiculo', 'placa_veiculo')
        }),
        ('Documentação', {
            'fields': ('cnh_numero', 'cnh_validade')
        }),
        ('Status e Aprovação', {
            'fields': ('status_aprovacao', 'online', 'observacoes_admin', 'data_aprovacao')
        }),
        ('Termos e Avaliações', {
            'fields': ('aceite_termos_voluntariado', 'data_aceite_termos', 'avaliacao_media', 'total_corridas')
        }),
    )

    def get_nome_usuario(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username

    get_nome_usuario.short_description = 'Nome do Usuário'


@admin.register(Corrida)
class CorridaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Corrida
    """
    list_display = ('id', 'get_paciente_nome', 'get_motorista_nome', 'status',
                    'data_hora_agendada', 'data_criacao')
    list_filter = ('status', 'necessita_cadeira_rodas', 'tem_acompanhante', 'data_criacao')
    search_fields = ('paciente__usuario__nome_completo',
                     'motorista__usuario__nome_completo',
                     'endereco_origem', 'endereco_destino')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    date_hierarchy = 'data_hora_agendada'

    fieldsets = (
        ('Participantes', {
            'fields': ('paciente', 'motorista')
        }),
        ('Endereços', {
            'fields': ('endereco_origem', 'latitude_origem', 'longitude_origem',
                       'endereco_destino', 'latitude_destino', 'longitude_destino')
        }),
        ('Agendamento', {
            'fields': ('data_hora_agendada', 'numero_passageiros', 'tem_acompanhante',
                       'necessita_cadeira_rodas', 'observacoes')
        }),
        ('Status e Controle', {
            'fields': ('status', 'data_hora_aceite', 'data_hora_inicio',
                       'data_hora_chegada', 'data_hora_finalizacao')
        }),
        ('Cancelamento', {
            'fields': ('motivo_cancelamento', 'data_cancelamento', 'cancelada_por')
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao')
        }),
    )

    def get_paciente_nome(self, obj):
        return obj.paciente.usuario.get_full_name() or obj.paciente.usuario.username

    get_paciente_nome.short_description = 'Paciente'

    def get_motorista_nome(self, obj):
        if obj.motorista:
            return obj.motorista.usuario.get_full_name() or obj.motorista.usuario.username
        return '-'

    get_motorista_nome.short_description = 'Motorista'


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Avaliacao
    """
    list_display = ('corrida', 'get_avaliador_nome', 'get_avaliado_nome',
                    'tipo_avaliacao', 'nota', 'data_avaliacao')
    list_filter = ('tipo_avaliacao', 'nota', 'data_avaliacao')
    search_fields = ('avaliador__nome_completo',
                     'avaliado__nome_completo', 'comentario')
    readonly_fields = ('data_avaliacao',)

    def get_avaliador_nome(self, obj):
        return obj.avaliador.get_full_name() or obj.avaliador.username

    get_avaliador_nome.short_description = 'Avaliador'

    def get_avaliado_nome(self, obj):
        return obj.avaliado.get_full_name() or obj.avaliado.username

    get_avaliado_nome.short_description = 'Avaliado'


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Notificacao
    """
    list_display = ('titulo', 'get_usuario_nome', 'tipo', 'lida', 'data_criacao')
    list_filter = ('tipo', 'lida', 'data_criacao')
    search_fields = ('titulo', 'mensagem', 'usuario__nome_completo')
    readonly_fields = ('data_criacao', 'data_leitura')

    def get_usuario_nome(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username

    get_usuario_nome.short_description = 'Usuário'


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Configuracao
    """
    list_display = ('chave', 'get_valor_resumo', 'descricao', 'data_atualizacao')
    search_fields = ('chave', 'valor', 'descricao')
    readonly_fields = ('data_atualizacao',)

    def get_valor_resumo(self, obj):
        valor_str = str(obj.valor)
        if len(valor_str) > 50:
            return f"{valor_str[:50]}..."
        return valor_str

    get_valor_resumo.short_description = 'Valor'
