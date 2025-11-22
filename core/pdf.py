from pathlib import Path

from django.conf import settings
from django.templatetags.static import static
from django.utils import timezone

from phases.models import Exercise, ExternalActivity, GuideStep, PhaseRelease


def resolve_static_base_url(request=None):
    """
    Retorna uma base absoluta para recursos estaticos.
    Quando houver request, gera uma URL HTTP; caso contrario, usa caminho file:// local.
    """
    if request:
        return request.build_absolute_uri(static("")).rstrip("/") + "/"

    candidates = []
    static_root = getattr(settings, "STATIC_ROOT", None)
    if static_root:
        candidates.append(static_root)
    candidates.extend(getattr(settings, "STATICFILES_DIRS", []))

    static_dir = None
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            static_dir = Path(candidate)
            break

    if not static_dir:
        static_dir = Path(settings.BASE_DIR) / "static"

    return static_dir.resolve().as_uri().rstrip("/") + "/"


def build_materials_context(static_base_url, generated_at=None):
    phase_infos = {pr.phase_number: pr for pr in PhaseRelease.objects.all()}
    return {
        "generated_at": generated_at or timezone.now(),
        "phase1_info": phase_infos.get(1),
        "phase2_info": phase_infos.get(2),
        "phase3_info": phase_infos.get(3),
        "phase4_info": phase_infos.get(4),
        "phase5_info": phase_infos.get(5),
        "exercises": Exercise.objects.filter(is_active=True).order_by("order"),
        "phase2_steps": GuideStep.objects.filter(phase=2).order_by("order"),
        "phase3_steps": GuideStep.objects.filter(phase=3).order_by("order"),
        "phase4_steps": GuideStep.objects.filter(phase=4).order_by("order"),
        "activities": ExternalActivity.objects.filter(is_active=True),
        "static_base_url": static_base_url,
    }
