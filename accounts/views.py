from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.db.models import Sum
from .forms import RegisterForm
from .models import UserProfile
from submissions.models import Submission

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
    submissions = Submission.objects.filter(user=request.user).order_by("-phase")
    total_score = submissions.aggregate(Sum('total_score'))['total_score__sum'] or 0
    context = {
        "profile": profile,
        "total_score": total_score,
        "submissions": submissions,
    }
    return render(request, "accounts/profile.html", context)
