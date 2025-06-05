from django.shortcuts import render, redirect
from .models import Agendamento
from django.contrib import messages
from .forms import AgendamentoForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404


def is_mecanico_or_admin(user):
    return user.is_authenticated and (user.groups.filter(name='Mecanico').exists() or user.is_superuser)

def home(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu serviço foi agendado! A data será confirmada e você receberá uma notificação por telefone.')
            return redirect('home')
    else:
        form = AgendamentoForm()

    return render(request, 'oficina/home.html', {'form': form})

def home(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_completo')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        veiculo = request.POST.get('veiculo')
        placa = request.POST.get('placa_do_veiculo')
        servico = request.POST.get('servico_desejado')
        data = request.POST.get('data_preferencial')
        horario = request.POST.get('horario_preferencial')
        observacoes = request.POST.get('observacoes')
        termos = request.POST.get('termos')

        if termos:  # Só salva se o usuário marcar o checkbox
            Agendamento.objects.create(
                nome_completo=nome,
                telefone=telefone,
                email=email,
                veiculo=veiculo,
                placa_do_veiculo=placa,
                servico_desejado=servico,
                data_preferencial=data,
                horario_preferencial=horario,
                observacoes=observacoes
            )
            return redirect('home')  # Redirecionar após salvar
        else:
            return render(request, 'home.html', {'erro': 'Você precisa aceitar os termos.'})

    return render(request, 'home.html')


@login_required
@user_passes_test(is_mecanico_or_admin)
@require_POST
def confirmar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
    agendamento.confirmado = True
    agendamento.mecanico_confirmador = request.user
    agendamento.save()
    return JsonResponse({'status': 'ok'})

