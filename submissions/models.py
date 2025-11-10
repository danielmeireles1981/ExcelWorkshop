from django.db import models
from django.contrib.auth.models import User

class Submission(models.Model):
    PHASE_CHOICES = (
        (1, "Fase 01 - Revisão"),
        (2, "Fase 02 - Orçamento"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phase = models.PositiveSmallIntegerField(choices=PHASE_CHOICES)
    exercise = models.ForeignKey("phases.Exercise", null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to="submissions/%Y/%m/%d/")
    feedback = models.TextField(blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_phase_display()} - {self.user.username} - #{self.id}"
