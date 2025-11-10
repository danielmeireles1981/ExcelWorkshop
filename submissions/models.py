from django.db import models
from django.conf import settings

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phase = models.PositiveIntegerField()
    file = models.FileField(upload_to="submissions/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)
    base_score = models.PositiveIntegerField(default=0)
    time_bonus = models.PositiveIntegerField(default=0)
    total_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Envio da Fase {self.phase} por {self.user.username}"