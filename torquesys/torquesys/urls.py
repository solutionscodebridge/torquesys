from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from oficina import views as oficina_views
from core import views as core_views

urlpatterns = [
    path('', oficina_views.home, name='home'),
    path('registrar-ponto/', core_views.registrar_ponto, name='registrar_ponto'),
    path('admin/', admin.site.urls),
    path('admin/custom-login/', core_views.admin_login_view, name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='logout'),
    path('cadastrar-peca/', core_views.cadastrar_peca, name='cadastrar_peca'),
]