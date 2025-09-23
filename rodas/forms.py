from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Paciente, Motorista


class PacienteRegisterForm(forms.Form):
    nome_completo = forms.CharField(max_length=150, label="Nome Completo")
    email = forms.EmailField(label="Email")
    cpf = forms.CharField(max_length=14, label="CPF")
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    responsavel_nome = forms.CharField(max_length=200, label="Nome do Responsável")
    responsavel_email = forms.EmailField(label="Email do Responsável")
    responsavel_telefone = forms.CharField(
        max_length=15, label="Telefone do Responsável"
    )
    responsavel_cpf = forms.CharField(max_length=14, label="CPF do Responsável")

    necessita_cadeira_rodas = forms.BooleanField(
        required=False, label="Necessita Cadeira de Rodas"
    )
    imunossuprimido = forms.BooleanField(required=False, label="Imunossuprimido")
    observacoes_medicas = forms.CharField(
        widget=forms.Textarea, required=False, label="Observações Médicas"
    )

    aceite_termos = forms.BooleanField(label="Aceite dos Termos de Uso")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        if Usuario.objects.filter(cpf=cpf).exists():
            raise ValidationError("Este CPF já está em uso.")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "As senhas não coincidem.")
        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                self.add_error("password1", e)
        return cleaned_data


class MotoristaRegisterForm(forms.Form):
    nome_completo = forms.CharField(max_length=150, label="Nome Completo")
    email = forms.EmailField(label="Email")
    cpf = forms.CharField(max_length=14, label="CPF")
    telefone = forms.CharField(max_length=15, label="Telefone")
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    marca_veiculo = forms.CharField(max_length=50, label="Marca do Veículo")
    modelo_veiculo = forms.CharField(max_length=50, label="Modelo do Veículo")
    cor_veiculo = forms.CharField(max_length=30, label="Cor do Veículo")
    ano_veiculo = forms.IntegerField(label="Ano do Veículo", required=False)
    placa_veiculo = forms.CharField(
        max_length=8, label="Placa do Veículo", required=False
    )

    cnh_numero = forms.CharField(max_length=20, label="Número da CNH", required=False)
    cnh_validade = forms.DateField(
        label="Validade da CNH",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    aceite_termos_voluntariado = forms.BooleanField(
        label="Aceite dos Termos de Voluntariado"
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        if Usuario.objects.filter(cpf=cpf).exists():
            raise ValidationError("Este CPF já está em uso.")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "As senhas não coincidem.")
        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                self.add_error("password1", e)
        return cleaned_data


class SolicitaCorridaform(forms.Form):
    endereco_origem = forms.CharField(max_length=255, label="Endereço de Origem")
    endereco_destino = forms.CharField(max_length=255, label="Endereço de Destino")
    data_agendamento = forms.DateField(label="Data")
    hora_agendamento = forms.TimeField(label="Hora")
