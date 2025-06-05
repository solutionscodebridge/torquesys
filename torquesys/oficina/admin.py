from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email', 'endereco')
    search_fields = ('nome', 'cpf', 'telefone')
    list_filter = ('nome',)
    ordering = ('nome',)
    list_per_page = 10


class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'modelo', 'placa', 'ano')
    search_fields = ('modelo', 'placa')
    list_filter = ('cliente',)
    ordering = ('modelo',)
    list_per_page = 10

class PecasAdmin(admin.ModelAdmin):
    list_display = ('peca', 'preco', 'quantidade_em_estoque', 'fornecedor')
    search_fields = ('descricao',)
    list_filter = ('peca',)
    ordering = ('peca',)
    list_per_page = 10

class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'proprietario', 'data', 'descricao', 'valor_estimado')
    search_fields = ('veiculo__modelo', 'proprietario__nome')
    list_filter = ('data',)
    ordering = ('data',)
    list_per_page = 10

class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'data_preferencial', 'horario_preferencial', 'nome_completo', 'telefone', 'servico_desejado', 'observacoes')
    search_fields = ('veiculo', 'nome_completo')
    ordering = ('data_preferencial',)
    list_per_page = 10


admin.site.register(Cliente, CustomerAdmin)
admin.site.register(Veiculo, VeiculoAdmin)
admin.site.register(Peca, PecasAdmin)
admin.site.register(Orcamento, OrcamentoAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.site_header = "Oficina Admin"
