from django.db import models
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User


# Validador de CPF e Telefone

def validar_telefone(value):
    padrao = r'^\(\d{2}\) \d{4,5}-\d{4}$'
    if not re.match(padrao, value):
        raise ValidationError(
            'O número de telefone deve estar no formato (DDD) XXXXX-XXXX.'
        )

# Expressão regular para validar CPF's
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    if int(cpf[9]) == digito1 and int(cpf[10]) == digito2:
        return True
    else:
        return False

def validar_cpf_model(value):
    if not validar_cpf(value):
        raise ValidationError('CPF inválido.')


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, validators=[validar_cpf_model])
    telefone = models.CharField(max_length=15, validators=[validar_telefone])
    email = models.EmailField()
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10)
    ano = models.IntegerField()

    def __str__(self):
        return f"{self.modelo} - {self.placa}"
    
class Peca(models.Model):
    peca = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_em_estoque = models.IntegerField()
    fornecedor = models.CharField(max_length=100)

    def __str__(self):
        return self.peca
    
class Orcamento(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    proprietario = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='orcamentos')
    data = models.DateField(auto_now_add=True)
    descricao = models.TextField()
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    pecas = models.ForeignKey(Peca, on_delete=models.CASCADE, related_name='orcamentos', null=True, blank=True)

    def __str__(self):
        return f"Orçamento para {self.veiculo} - {self.data} - cliente: {self.proprietario.nome}"

class Agendamento(models.Model):
      SERVICOS_PRESTADOS = [
          ('troca_oleo', 'Troca de Óleo'),
          ('sistema_eletrico', 'Sistema Elétrico'),
          ('mecanica_geral', 'Mecânica Geral'),
          ('injecao_eletronica', 'Injeção Eletrônica'),
          ('alinhamento_balanceamento', 'Alinhamento e Balanceamento'),
          ('ar_condicionado', 'Ar Condicionado'),
          ('outro', 'Outro'),
      ]
      nome_completo = models.CharField(max_length=100)
      telefone = models.CharField(max_length=15, validators=[validar_telefone])
      email = models.EmailField()
      veiculo = models.CharField(max_length=50, blank=True, null=True, verbose_name='Descreva o modelo do veículo')
      placa_do_veiculo = models.CharField(max_length=10, blank=True, null=True, verbose_name='Placa do veículo')
      servico_desejado = models.CharField(max_length=30, choices=SERVICOS_PRESTADOS, verbose_name='Serviço desejado')
      data_preferencial = models.DateField(verbose_name='Data preferencial')
      horario_preferencial = models.TimeField(verbose_name='Horário preferencial')
      observacoes = models.TextField(blank=True, null=True, verbose_name='Descreva o problema ou informe detalhes adicionais')
      confirmado = models.BooleanField(default=False)  # novo campo para controlar confirmação
      mecanico_confirmador = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='confirmacoes')
      confirmado = models.BooleanField(default=False)

      def __str__(self):
          return f"Agendamento: {self.nome_completo} - {self.data_preferencial} - {self.horario_preferencial}"
    
    