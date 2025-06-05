from django import forms
from oficina.models import Peca


class PecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = ['peca', 'preco', 'fornecedor', 'quantidade_em_estoque']
