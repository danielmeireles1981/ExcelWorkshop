from django.contrib import admin
from .models import PhaseRelease, Exercise, GuideStep, ExternalActivity, UserPhaseAttempt, QuizQuestion

@admin.register(PhaseRelease)
class PhaseReleaseAdmin(admin.ModelAdmin):
    list_display = ('phase_number', 'is_released', 'duration_minutes')
    list_editable = ('is_released', 'duration_minutes')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('phase_number', 'question_text', 'answer_text')
    list_filter = ('phase_number',)
    search_fields = ('question_text',)

admin.site.register(Exercise)
admin.site.register(GuideStep)
admin.site.register(ExternalActivity)
admin.site.register(UserPhaseAttempt)