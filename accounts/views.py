import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .forms import (
    RegisterForm,
    HERO_VILLAIN_CHOICES,
    EXCEL_EXPERIENCE_CHOICES,
)
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
                favorite_character=form.cleaned_data.get("favorite_character", ""),
                excel_experience=form.cleaned_data.get("excel_experience", ""),
            )
            login(request, user)
            messages.success(
                request,
                "Cadastro realizado com sucesso! Veja abaixo a explicação dos perfis.",
            )
            return redirect("accounts:profile")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def profile(request):
    profile = getattr(request.user, "profile", None)
    submissions = Submission.objects.filter(user=request.user).order_by("-phase")
    context = {
        "profile": profile,
        "submissions": submissions,
    }
    return render(request, "accounts/profile.html", context)


def _flatten_choices(choices):
    flat = []
    for value, label in choices:
        if isinstance(label, (list, tuple)):
            for v, l in label:
                flat.append((v, l))
        else:
            flat.append((value, label))
    return flat


@staff_member_required
def registration_stats(request):
    # Personagens favoritos (DC/Marvel)
    character_counts_qs = (
        UserProfile.objects.exclude(favorite_character="")
        .values("favorite_character")
        .annotate(total=Count("id"))
    )
    character_counts = {
        row["favorite_character"]: row["total"] for row in character_counts_qs
    }

    flat_char_choices = [
        (value, label)
        for value, label in _flatten_choices(HERO_VILLAIN_CHOICES)
        if value
    ]
    character_labels = [label for value, label in flat_char_choices]
    character_data = [character_counts.get(value, 0) for value, _ in flat_char_choices]

    # Perfil profissional
    profile_counts_qs = (
        UserProfile.objects.values("professional_profile")
        .annotate(total=Count("id"))
        .order_by()
    )
    profile_counts = {
        row["professional_profile"]: row["total"] for row in profile_counts_qs
    }
    profile_labels = [label for value, label in UserProfile.ProfessionalProfile.choices]
    profile_data = [
        profile_counts.get(value, 0)
        for value, _ in UserProfile.ProfessionalProfile.choices
    ]

    # Nível de Excel
    excel_counts_qs = (
        UserProfile.objects.exclude(excel_experience="")
        .values("excel_experience")
        .annotate(total=Count("id"))
    )
    excel_counts = {row["excel_experience"]: row["total"] for row in excel_counts_qs}
    flat_excel_choices = list(EXCEL_EXPERIENCE_CHOICES)
    excel_labels = [label for value, label in flat_excel_choices]
    excel_data = [excel_counts.get(value, 0) for value, _ in flat_excel_choices]

    context = {
        "character_labels": mark_safe(json.dumps(character_labels)),
        "character_data": mark_safe(json.dumps(character_data)),
        "profile_labels": mark_safe(json.dumps(profile_labels)),
        "profile_data": mark_safe(json.dumps(profile_data)),
        "excel_labels": mark_safe(json.dumps(excel_labels)),
        "excel_data": mark_safe(json.dumps(excel_data)),
    }
    return render(request, "accounts/registration_stats.html", context)

