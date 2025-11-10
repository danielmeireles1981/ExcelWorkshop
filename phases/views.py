from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from .models import Exercise, GuideStep, ExternalActivity, PhaseRelease, UserPhaseAttempt
from .decorators import phase_released_required
from .forms import UploadAnswerForm
from submissions.models import Submission

def _calculate_score(user, phase_number, submission):
    """Calcula a pontuação base e o bônus de tempo."""
    base_score = 100
    time_bonus = 0

    try:
        attempt = UserPhaseAttempt.objects.get(user=user, phase_number=phase_number)
        release = PhaseRelease.objects.get(phase_number=phase_number)
        
        time_limit = attempt.start_time + timedelta(minutes=release.duration_minutes)
        
        if submission.created_at <= time_limit:
            time_bonus = 50 # Bônus fixo por entregar no tempo

    except (UserPhaseAttempt.DoesNotExist, PhaseRelease.DoesNotExist):
        pass # Se não houver registro de tentativa ou liberação, não há bônus

    submission.base_score = base_score
    submission.time_bonus = time_bonus
    submission.total_score = base_score + time_bonus

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
            _calculate_score(request.user, 1, submission)
            submission.save()
            messages.success(request, f"Fase 01 enviada! Você ganhou {submission.total_score} pontos!")
            return redirect("phases:phase1_index")
    else:
        form = UploadAnswerForm()

    exercises = Exercise.objects.filter(is_active=True).order_by("order")
    return render(request, "phases/phase1_index.html", {"exercises": exercises, "form": form})

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
            _calculate_score(request.user, 2, submission)
            submission.save()
            messages.success(request, f"Fase 02 enviada! Você ganhou {submission.total_score} pontos! 🎉")
            return redirect("phases:phase2_guide")
    else:
        form = UploadAnswerForm()
    return render(request, "phases/phase2_guide.html", {"steps": steps, "form": form})

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
            _calculate_score(request.user, 3, submission)
            submission.save()
            messages.success(request, f"Fase 03 enviada! Você ganhou {submission.total_score} pontos! 🚀")
            return redirect("phases:phase3_index")
    else:
        form = UploadAnswerForm()
    return render(request, "phases/phase3_index.html", {"steps": steps, "form": form})

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
            _calculate_score(request.user, 4, submission)
            submission.save()
            messages.success(request, f"Desafio final entregue! Você ganhou {submission.total_score} pontos! 🌟")
            return redirect("phases:phase4_index")
    else:
        form = UploadAnswerForm()
    return render(request, "phases/phase4_index.html", {"steps": steps, "form": form})

@login_required
@phase_released_required(5)
def phase5_index(request):
    activities = ExternalActivity.objects.filter(is_active=True)
    return render(request, "phases/phase5_index.html", {"activities": activities})
