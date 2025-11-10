from django.contrib import admin
from .models import PhaseRelease, Exercise, GuideStep, ExternalActivity, UserPhaseAttempt

@admin.register(PhaseRelease)
class PhaseReleaseAdmin(admin.ModelAdmin):
    list_display = ('phase_number', 'is_released', 'duration_minutes')
    list_editable = ('is_released', 'duration_minutes')

admin.site.register(Exercise)
admin.site.register(GuideStep)
admin.site.register(ExternalActivity)
admin.site.register(UserPhaseAttempt) # Opcional, mas útil para debug