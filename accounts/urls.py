from django.urls import path

from .views import SignInView, SignOutView, register, profile, registration_stats

app_name = "accounts"

urlpatterns = [
    path("login/", SignInView.as_view(), name="login"),
    path("logout/", SignOutView.as_view(), name="logout"),
    path("cadastro/", register, name="register"),
    path("perfil/", profile, name="profile"),
    path(
        "relatorio-cadastros/",
        registration_stats,
        name="registration_stats",
    ),
]
