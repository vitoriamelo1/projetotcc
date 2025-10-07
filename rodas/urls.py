from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "rodas"

urlpatterns = [
    # Páginas públicas
    path("", views.index, name="index"),
    path("sobre/", views.sobre, name="sobre"),
    path("contato/", views.contato, name="contato"),
    # Autenticação
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path(
        "register/motorista/", views.register_motorista_view, name="register_motorista"
    ),
    path("password-reset/", views.password_reset_view, name="password_reset"),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="rodas/auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="rodas/auth/password_reset_confirm.html",
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="rodas/auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Áreas restritas
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("solicita-corrida/", views.solicitar_corrida_view, name="solicita_corrida"),
    # Corridas
    path(
        "corrida/<int:corrida_id>/",
        views.corrida_detalhes_view,
        name="corrida_detalhes",
    ),
    # API endpoints
    path(
        "api/corridas/<int:corrida_id>/aceitar/",
        views.aceitar_corrida_view,
        name="aceitar_corrida",
    ),
    path(
        "api/motorista/toggle-status/",
        views.toggle_motorista_status_view,
        name="toggle_motorista_status",
    ),
    path(
        "api/corridas/<int:corrida_id>/status/",
        views.atualizar_status_corrida_view,
        name="atualizar_status_corrida",
    ),
]
