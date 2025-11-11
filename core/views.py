from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth import get_user_model
from submissions.models import Submission

from phases.models import PhaseRelease
User = get_user_model()

def home(request):
    if request.user.is_authenticated:
        all_phases = [
            {'number': 1, 'title': 'Fase 01 — Revisão', 'url_name': 'phases:phase1_index'},
            {'number': 2, 'title': 'Fase 02 — Controle de Estoque', 'url_name': 'phases:phase2_guide'},
            {'number': 3, 'title': 'Fase 03 — Gratificação', 'url_name': 'phases:phase3_index'},
            {'number': 4, 'title': 'Fase 04 — Desafio Final', 'url_name': 'phases:phase4_index'},
            {'number': 5, 'title': 'Fase 05 — Encerramento', 'url_name': 'phases:phase5_index'},
        ]

        # Busca as configurações de duração de todas as fases em uma única consulta
        phase_releases = {pr.phase_number: pr for pr in PhaseRelease.objects.all()}

        # Adiciona a duração a cada fase
        for phase in all_phases:
            release_info = phase_releases.get(phase['number'])
            phase['duration'] = release_info.duration_minutes if release_info else 60

        if request.user.is_staff:
            visible_phases = all_phases
        else:
            released_phases_numbers = {num for num, pr in phase_releases.items() if pr.is_released}
            visible_phases = [phase for phase in all_phases if phase['number'] in released_phases_numbers]

        completed_phases = set(Submission.objects.filter(user=request.user).values_list('phase', flat=True))
        
        context = {
            'visible_phases': visible_phases,
            'completed_phases': completed_phases,
        }
        return render(request, "core/home.html", context)

    return render(request, "core/landing.html")

@login_required
def ranking(request):
    """Exibe o ranking de usuários com base na pontuação total."""
    # Usamos select_related('profile') para buscar o perfil do usuário na mesma consulta
    users_ranked = User.objects.select_related('profile').annotate(
        total_score=Sum('submission__total_score')
    ).filter(
        total_score__gt=0
    ).order_by('-total_score')

    context = {'users_ranked': users_ranked}
    return render(request, "core/ranking.html", context)
