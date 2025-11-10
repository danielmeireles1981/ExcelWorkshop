from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Exercise, GuideStep, ExternalActivity
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
            messages.success(request, "Arquivo da Fase 01 enviado com sucesso!")
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
    steps = GuideStep.objects.filter(phase=2).order_by("order")
    if request.method == "POST":
        form = UploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.phase = 2
            submission.save()
            messages.success(request, "Planilha enviada com sucesso! 🎉")
            return redirect("phases:phase2_guide")
    else:
        form = UploadAnswerForm()
    return render(request, "phases/phase2_guide.html", {"steps": steps, "form": form})

@login_required
@phase_released_required(3)
def phase3_index(request):
    steps = GuideStep.objects.filter(phase=3).order_by("order")
    if request.method == "POST":
        form = UploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.phase = 3
            submission.save()
            messages.success(request, "Planilha da Fase 03 enviada com sucesso! 🚀")
            return redirect("phases:phase3_index")
    else:
        form = UploadAnswerForm()
    return render(request, "phases/phase3_index.html", {"steps": steps, "form": form})

@login_required
@phase_released_required(4)
def phase4_index(request):
    steps = GuideStep.objects.filter(phase=4).order_by("order")
    if request.method == "POST":
        form = UploadAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.phase = 4
            submission.save()
            messages.success(request, "Desafio final entregue! Você é uma estrela do Excel! 🌟")
            return redirect("phases:phase4_index")
    else:
        form = UploadAnswerForm()
    return render(request, "phases/phase4_index.html", {"steps": steps, "form": form})

@login_required
@phase_released_required(5)
def phase5_index(request):
    activities = ExternalActivity.objects.filter(is_active=True)
    return render(request, "phases/phase5_index.html", {"activities": activities})
