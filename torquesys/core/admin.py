from django.contrib import admin
from .models import Colaborador, FolhaDePagamento, Ferias, Afastamento, Treinamento, Ponto

# Registrando o modelo de Colaborador
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome_do_funcionario', 'cargo_do_colaborador', 'departamento', 'status', 'data_de_contratacao', 'salario')
    search_fields = ['nome_do_funcionario', 'matricula', 'cpf']
    list_filter = ['departamento', 'status', 'data_de_contratacao']
    ordering = ['nome_do_funcionario']
    list_per_page = 20



# Registrando o modelo de Folha de Pagamento
class FolhaDePagamentoAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'salario_base', 'horas_extras', 'descontos', 'valor_liquido', 'mes_ano')
    search_fields = ['colaborador__nome_do_funcionario', 'mes_ano']
    list_filter = ['mes_ano']
    ordering = ['mes_ano']
    list_per_page = 20



# Registrando o modelo de Férias
class FeriasAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'data_inicio', 'data_fim', 'dias_utilizados', 'status')
    search_fields = ['colaborador__nome_do_funcionario']
    list_filter = ['status']
    ordering = ['data_inicio']
    list_per_page = 20



# Registrando o modelo de Afastamento
class AfastamentoAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'data_inicio', 'data_fim', 'motivo', 'status')
    search_fields = ['colaborador__nome_do_funcionario', 'motivo']
    list_filter = ['status']
    ordering = ['data_inicio']
    list_per_page = 20



# Registrando o modelo de Treinamento
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'nome_treinamento', 'data_inicio', 'data_fim', 'certificado')
    search_fields = ['colaborador__nome_do_funcionario', 'nome_treinamento']
    list_filter = ['certificado']
    ordering = ['data_inicio']
    list_per_page = 20



# Registrando o modelo de Ponto
class PontoAdmin(admin.ModelAdmin):
    list_display = ('colaborador', 'data', 'hora_entrada', 'hora_saida', 'status')
    search_fields = ['colaborador__username', 'data']
    list_filter = ['status']
    ordering = ['data']
    list_per_page = 20


admin.site.register(Colaborador, ColaboradorAdmin)
admin.site.register(FolhaDePagamento, FolhaDePagamentoAdmin)
admin.site.register(Ferias, FeriasAdmin)
admin.site.register(Afastamento, AfastamentoAdmin)
admin.site.register(Treinamento, TreinamentoAdmin)
admin.site.register(Ponto, PontoAdmin)