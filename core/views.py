from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from submissions.models import Submission

from phases.models import PhaseRelease

def home(request):
    if request.user.is_authenticated:
        all_phases = [
            {'number': 1, 'title': 'Fase 01 — Revisão', 'url_name': 'phases:phase1_index'},
            {'number': 2, 'title': 'Fase 02 — Controle de Estoque', 'url_name': 'phases:phase2_guide'},
            {'number': 3, 'title': 'Fase 03 — Gratificação', 'url_name': 'phases:phase3_index'},
            {'number': 4, 'title': 'Fase 04 — Desafio Final', 'url_name': 'phases:phase4_index'},
            {'number': 5, 'title': 'Fase 05 — Encerramento', 'url_name': 'phases:phase5_index'},
        ]

        if request.user.is_staff:
            visible_phases = all_phases
        else:
            released_phases_numbers = set(PhaseRelease.objects.filter(is_released=True).values_list('phase_number', flat=True))
            visible_phases = [phase for phase in all_phases if phase['number'] in released_phases_numbers]

        completed_phases = set(Submission.objects.filter(user=request.user).values_list('phase', flat=True))
        
        context = {
            'visible_phases': visible_phases,
            'completed_phases': completed_phases,
        }
        return render(request, "core/home.html", context)

    return render(request, "core/landing.html")
