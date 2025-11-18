from django.db import models
from django.conf import settings


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phase = models.PositiveIntegerField()
    file = models.FileField(upload_to="submissions/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Envio da Fase {self.phase} por {self.user.username}"
