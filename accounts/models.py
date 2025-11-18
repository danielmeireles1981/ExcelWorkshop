from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    class ProfessionalProfile(models.TextChoices):
        ESTUDANTE = "EST", "Estudante"
        EMPREENDEDOR_JR = "EMPJ", "Empreendedor Júnior"
        ANALISTA_JR = "ANJ", "Analista de Dados Jr."
        FINANCEIRO = "FIN", "Assistente Financeiro"
        OUTRO = "OUT", "Outro"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar_emoji = models.CharField(max_length=8, default="😀")
    professional_profile = models.CharField(
        max_length=5,
        choices=ProfessionalProfile.choices,
        default=ProfessionalProfile.ESTUDANTE,
    )
    favorite_character = models.CharField(
        max_length=60,
        blank=True,
        help_text="Personagem herói ou vilão de DC ou Marvel.",
    )
    excel_experience = models.CharField(
        max_length=20,
        blank=True,
        help_text="Nível de experiência em Excel.",
    )
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

