from django.db import models
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User


#######------------- Funções gerais para validação de itens dentro da model -------------####

# Expressão regular para validar telefones no formato brasileiro
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


#######------------- Classes da model que aparecerão dentro do painel administrativo do django -------------####


# Cadastro de Colaboradores
class Colaborador(models.Model):
        DEPARTAMENTO_CHOICES = (
            ("RH", "RECURSOS HUMANOS"),
            ("VE", "VENDAS"),
            ("MEC", "MECANICOS"),
            ("ADM", "ADMINISTRATIVO"),
            ("TI", "TECNOLOGIA DA INFORMAÇÃO"),
        )
         
        STATUS_CHOICES = (
        ("ATIVO", "Ativo"),
        ("AFASTADO", "Afastado"),
        ("DEMITIDO", "Demitido"),
        ("FERIAS", "Férias"),

        )

        nome_do_funcionario = models.CharField(max_length=50, verbose_name="Escreva o nome completo do Colaborador.")
        data_de_nascimento = models.DateField()
        endereco = models.CharField(max_length=255, verbose_name="Endereço do Colaborador")
        cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF do Colaborador", validators=[validar_cpf_model])
        matricula = models.CharField(max_length=50)
        data_de_contratacao = models.DateField()
        numero_telefone_colaborador = models.CharField(
            max_length=15,
            validators=[validar_telefone],  # Aplica a validação
            verbose_name='Nº telefone celular'
        )
        email_colaborador = models.EmailField(max_length=100, verbose_name="Insira o e-mail do colaborador")
        departamento = models.CharField(max_length=4, choices=DEPARTAMENTO_CHOICES, blank=True, null=False)
        cargo_do_colaborador = models.CharField(max_length=40, verbose_name="Cargo do Colaborador")
        status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ATIVO")
        foto_perfil = models.ImageField(upload_to='colaboradores/', null=True, blank=True, verbose_name="Foto de Perfil")
        salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salário do Colaborador")
        horario_trabalho = models.CharField(max_length=50, verbose_name="Horário de Trabalho")
        avaliacao_desempenho = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Avaliação de Desempenho")


        def __str__(self):
            return self.nome_do_funcionario
        
# Registros de folhas de pagamento por colaborador
class FolhaDePagamento(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    horas_extras = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descontos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    mes_ano = models.DateField()

    def calcular_salario_liquido(self):
        # Lógica para calcular o salário líquido
        return self.salario_base + self.horas_extras - self.descontos

    def __str__(self):
        return f"{self.colaborador.nome} - {self.mes_ano.strftime('%m/%Y')}"
    
#Adicionar Férias ao colaborador
class Ferias(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    dias_utilizados = models.PositiveIntegerField()  # Exemplo: 30 dias
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('aprovado', 'Aprovado'), ('cancelado', 'Cancelado')])

    def __str__(self):
        return f"Férias {self.colaborador.nome} - {self.status}"

# Lançamento de Atestado por colaborador
class Afastamento(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)  # Se ainda estiver em afastamento, pode ser deixado em branco
    motivo = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('em_andamento', 'Em Andamento'), ('finalizado', 'Finalizado')])

    def __str__(self):
        return f"Afastamento {self.colaborador.nome} - {self.motivo}"


# Treinamentos, Cursos e Especializações
class Treinamento(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    nome_treinamento = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    certificado = models.BooleanField(default=False)

    def __str__(self):
        return f"Treinamento {self.nome_treinamento} - {self.colaborador.nome}"


# Model de Registro de ponto de colaboradores:
class Ponto(models.Model):
    colaborador = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('saida', 'Saída')], default='entrada')
    data = models.DateTimeField(auto_now_add=True)
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_saida = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default='pendente')

    def __str__(self):
        return f'{self.colaborador.username} - {self.tipo}'
    

