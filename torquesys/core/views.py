from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Ponto
from django.utils import timezone
from .forms import PecaForm

def home(request):
    return render(request, 'home.html')


# View para o login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirecionar para a página principal ou dashboard
            else:
                form.add_error(None, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'admin/login.html', {'form': form})


@login_required
def registrar_ponto(request):
    if request.method == 'POST':
        ultimo_ponto = Ponto.objects.filter(colaborador=request.user).last()

        if not ultimo_ponto or ultimo_ponto.tipo == 'saida':
            Ponto.objects.create(colaborador=request.user, tipo='entrada', hora_entrada=timezone.now())
            status_text = "Entrada registrada com sucesso!"
        else:
            Ponto.objects.create(colaborador=request.user, tipo='saida', hora_saida=timezone.now())
            status_text = "Saída registrada com sucesso!"

        return render(request, 'registration/registrar_ponto.html', {'status_text': status_text})

    return render(request, 'registration/registrar_ponto.html', {'status_text': "Por favor, registre seu ponto."})


# View para visualizar os registros de ponto
@login_required
def historico_ponto(request):
    # Filtra os pontos registrados pelo usuário logado
    pontos = Ponto.objects.filter(colaborador=request.user)
    return render(request, 'registration/historico_ponto.html', {'pontos': pontos})


# View de Login para o admin personalizado
def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Ou para a página que você deseja redirecionar após o login
            else:
                form.add_error(None, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()

    return render(request, 'admin/custom_login.html', {'form': form})

@login_required
def cadastrar_peca(request):
    if request.method == "POST":
        form = PecaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucesso_cadastro')  # Redireciona para uma página de sucesso após o cadastro
    else:
        form = PecaForm()
    
    return render(request, 'peca/cadastrar_peca.html', {'form': form})


