from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils import timezone

from .models import (
    Exercise,
    GuideStep,
    ExternalActivity,
    PhaseRelease,
    UserPhaseAttempt,
    QuizQuestion,
)
from .decorators import phase_released_required
from .forms import UploadAnswerForm
from submissions.models import Submission


@login_required
@phase_released_required(1)
def phase1_index(request):
    if request.method == "POST":
        form = UploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.phase = 1
            # Não associamos a um exercício específico, pois é um envio para a fase toda.
            submission.save()
            messages.success(request, "Fase 01 enviada com sucesso!")
            return redirect("phases:phase1_index")
    else:
        form = UploadAnswerForm()

    phase_info = PhaseRelease.objects.filter(phase_number=1).first()
    exercises = Exercise.objects.filter(is_active=True).order_by("order")
    context = {
        "phase_info": phase_info,
        "exercises": exercises,
        "form": form,
    }
    return render(request, "phases/phase1_index.html", context)


@login_required
def all_phases_quiz_view(request):
    """Exibe todas as perguntas do quiz de todas as fases como flip cards."""
    if not request.user.is_staff:
        messages.error(request, "Esta área é restrita para administradores.")
        return redirect("core:home")

    questions = QuizQuestion.objects.all().order_by("?")  # Ordem aleatória
    context = {
        "questions": questions,
    }
    return render(request, "phases/all_phases_quiz.html", context)


@login_required
@phase_released_required(1)
def exercise_detail(request, slug):
    """
    Esta view agora serve apenas para exibir os detalhes de um exercício,
    sem a funcionalidade de envio.
    """
    exercise = get_object_or_404(Exercise, slug=slug, is_active=True)
    return render(request, "phases/exercise_detail.html", {"exercise": exercise})


@login_required
@phase_released_required(1)
def get_exercise_details_json(request, slug):
    """
    Retorna os detalhes de um exercício em formato JSON.
    Usado para popular o modal na página da Fase 01.
    """
    exercise = get_object_or_404(Exercise, slug=slug, is_active=True)
    data = {
        "title": exercise.title,
        "description": exercise.description,
        "reference_formula": exercise.reference_formula,
    }
    return JsonResponse(data)


@login_required
@phase_released_required(2)
def phase2_guide(request):
    UserPhaseAttempt.objects.get_or_create(user=request.user, phase_number=2)
    steps = GuideStep.objects.filter(phase=2).order_by("order")
    if request.method == "POST":
        form = UploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.created_at = timezone.now()
            submission.user = request.user
            submission.phase = 2
            submission.save()
            messages.success(request, "Fase 02 enviada com sucesso!")
            return redirect("phases:phase2_guide")
    else:
        form = UploadAnswerForm()

    phase_info = PhaseRelease.objects.filter(phase_number=2).first()
    context = {
        "steps": steps,
        "form": form,
        "phase_info": phase_info,
    }
    return render(request, "phases/phase2_guide.html", context)


@login_required
@phase_released_required(3)
def phase3_index(request):
    UserPhaseAttempt.objects.get_or_create(user=request.user, phase_number=3)
    steps = GuideStep.objects.filter(phase=3).order_by("order")
    if request.method == "POST":
        form = UploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.created_at = timezone.now()
            submission.user = request.user
            submission.phase = 3
            submission.save()
            messages.success(request, "Fase 03 enviada com sucesso!")
            return redirect("phases:phase3_index")
    else:
        form = UploadAnswerForm()

    phase_info = PhaseRelease.objects.filter(phase_number=3).first()
    context = {
        "steps": steps,
        "form": form,
        "phase_info": phase_info,
    }
    return render(request, "phases/phase3_index.html", context)


@login_required
@phase_released_required(4)
def phase4_index(request):
    UserPhaseAttempt.objects.get_or_create(user=request.user, phase_number=4)
    steps = GuideStep.objects.filter(phase=4).order_by("order")
    if request.method == "POST":
        form = UploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.created_at = timezone.now()
            submission.user = request.user
            submission.phase = 4
            submission.save()
            messages.success(request, "Desafio final entregue com sucesso!")
            return redirect("phases:phase4_index")
    else:
        form = UploadAnswerForm()

    phase_info = PhaseRelease.objects.filter(phase_number=4).first()
    context = {
        "steps": steps,
        "form": form,
        "phase_info": phase_info,
    }
    return render(request, "phases/phase4_index.html", context)


@login_required
@phase_released_required(5)
def phase5_index(request):  # Não há formulário de envio para a Fase 5
    activities = ExternalActivity.objects.filter(is_active=True)
    phase_info = PhaseRelease.objects.filter(phase_number=5).first()
    context = {
        "activities": activities,
        "phase_info": phase_info,
    }
    return render(request, "phases/phase5_index.html", context)

