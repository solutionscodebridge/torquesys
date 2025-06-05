# oficina/forms.py
from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'  # ou especifique os campos que você quer incluir

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data_preferencial')
        horario = cleaned_data.get('horario_preferencial')

        # Validação para não permitir horários já ocupados
        if data and horario:
            if Agendamento.objects.filter(data_preferencial=data, horario_preferencial=horario).exists():
                raise forms.ValidationError('Este horário já está agendado. Por favor, escolha outro.')

        return cleaned_data
