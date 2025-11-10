from django.db import models
from django.conf import settings

class Exercise(models.Model):
    """Exercícios da Fase 01, ligados às funções do arquivo aula00.pdf."""
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    reference_formula = models.CharField(max_length=40)  # e.g. SOMASE, PROCV
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.order}] {self.title}"

class GuideStep(models.Model):
    """Passo a passo da Fase 02: orçamento financeiro pessoal."""
    order = models.PositiveIntegerField(default=1)
    phase = models.PositiveIntegerField(default=2)
    title = models.CharField(max_length=120)
    instructions = models.TextField()

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return f"Fase {self.phase} - Passo {self.order}. {self.title}"

class ExternalActivity(models.Model):
    PROVIDERS = (
        ("kahoot", "Kahoot"),
        ("genially", "Genially"),
    )
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    title = models.CharField(max_length=150)
    url = models.URLField()
    embed_html = models.TextField(blank=True, help_text="Cole o iframe/HTML incorporável, se houver.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_provider_display()} — {self.title}"

class UserPhaseAttempt(models.Model):
    """Registra quando um usuário inicia uma fase para controle de tempo."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phase_number = models.PositiveIntegerField()
    start_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'phase_number') # Garante que só há um registro de início por usuário/fase

    def __str__(self):
        return f"Tentativa de {self.user.username} na Fase {self.phase_number}"

class PhaseRelease(models.Model):
    """Controla a liberação de cada fase para os usuários."""
    phase_number = models.PositiveIntegerField(unique=True, verbose_name="Número da Fase")
    is_released = models.BooleanField(default=False, verbose_name="Liberada para todos os usuários?")
    duration_minutes = models.PositiveIntegerField(default=60, verbose_name="Duração da Fase (minutos)")

    class Meta:
        ordering = ('phase_number',)
        verbose_name = "Liberação de Fase"
        verbose_name_plural = "Liberações de Fases"

    def __str__(self):
        return f"Fase {self.phase_number} - {'Liberada' if self.is_released else 'Bloqueada'}"
