# EDITADO - ABRIL/2

from . import views
from django.urls         import path, reverse_lazy
from django.shortcuts    import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',                              lambda request: redirect('login'),  name='home'),  # Redireciona para login
    path('login/',                        views.login_view,                   name='login'),
    path('dashboard/',                    views.dashboard_view,               name='dashboard'),
    path('cadastro/',                     views.cadastro_view,                name='cadastro'),

    path('projetos/',                     views.projetos_view,                name='projetos'),
   

    # PROJETOS
    path('projetos/', views.projetos_view, name='projetos'),
    path('novo_projeto/', views.novo_projeto_view, name='novo_projeto'),
    # Use nomes únicos para cada recurso
    path('projetos/gerenciar_itens/', views.GerenciarItensView.as_view(), {'resource': 'projetos'}, name='gerenciar_itens_projetos'),

    # CUSTOS FIXOS
    path('custos_fixos/', views.custos_fixos_view, name='custos_fixos'),
    path('custos_fixos/gerenciar_itens/', views.GerenciarItensView.as_view(), {'resource': 'custos_fixos'}, name='gerenciar_itens_custos'),
    path('custos_fixos/gerenciar_itens/<int:id>/', views.GerenciarItensView.as_view(), {'resource': 'custos_fixos'}, name='gerenciar_itens_custos_edit'),
    
    # IMPOSTOS
    path('impostos/', views.impostos_view, name='impostos'),
    path('impostos/gerenciar_itens/', views.GerenciarItensView.as_view(), {'resource': 'impostos'}, name='gerenciar_itens_impostos'),
    path('impostos/gerenciar_itens/<int:id>/', views.GerenciarItensView.as_view(), {'resource': 'impostos'}, name='gerenciar_itens_impostos_edit'),

    # CONFIGURACOES
    path('configuracoes/', views.configuracoes_view, name='configuracoes'),
    
    path('buscar_notificacoes/', views.buscar_notificacoes_ajax, name='buscar_notificacoes'),

    path('exportar_projeto_pdf/<int:id>/<str:currency>/', views.exportar_projeto_pdf, name='exportar_projeto_pdf'),

    path('logout/',                       auth_views.LogoutView.as_view(),    name='logout'),

    # =============== REDEFINIR A SENHA ========================================= #
    path('esqueci-minha-senha/',          views.CustomPasswordResetView.as_view(), name='password_reset'), # password_reset_form.html

    path('esqueci-minha-senha/enviado/', 
        auth_views.PasswordResetDoneView.as_view(template_name='redefinir_senha/password_reset_done.html'),
        name='password_reset_done'),

    path('redefinir-senha/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='redefinir_senha/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ), name='password_reset_confirm'),

    path('redefinir-senha/concluido/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='redefinir_senha/password_reset_complete.html'),
        name='password_reset_complete'),
    # =========================================================================== #
]