from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import PhaseRelease

def phase_released_required(phase_number):
    """
    Decorator que verifica se uma fase foi liberada para usuários comuns.
    Admins (staff) sempre têm acesso.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_staff:
                is_released = PhaseRelease.objects.filter(phase_number=phase_number, is_released=True).exists()
                if not is_released:
                    messages.error(request, f"A Fase {phase_number} ainda não foi liberada.")
                    return redirect("core:home")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator