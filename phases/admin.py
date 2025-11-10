from django.contrib import admin
from .models import PhaseRelease, Exercise, GuideStep, ExternalActivity

@admin.register(PhaseRelease)
class PhaseReleaseAdmin(admin.ModelAdmin):
    list_display = ('phase_number', 'is_released')
    list_editable = ('is_released',)

admin.site.register(Exercise)
admin.site.register(GuideStep)
admin.site.register(ExternalActivity)