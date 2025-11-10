from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from .forms import RegisterForm
from .models import UserProfile

class SignInView(LoginView):
    template_name = "accounts/login.html" 

class SignOutView(LogoutView):
    next_page = "core:home"


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # cria perfil
            UserProfile.objects.create(
                user=user,
                avatar_emoji=form.cleaned_data["avatar_emoji"],
                professional_profile=form.cleaned_data["professional_profile"],
            )
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso! Veja abaixo a explicação dos perfis.")
            return redirect("accounts:profile")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def profile(request):
    profile = getattr(request.user, "profile", None)
    return render(request, "accounts/profile.html", {"profile": profile})
