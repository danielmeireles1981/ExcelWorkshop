from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


EMOJI_CHOICES = [
    "😀",
    "😎",
    "🤓",
    "🧠",
    "🚀",
    "🐱",
    "🐶",
    "🧑‍💻",
    "🧙‍♂️",
    "🤖",
]

HERO_VILLAIN_CHOICES = [
    ("", "Selecione um personagem..."),
    (
        "DC - Heróis",
        [
            ("batman", "Batman (DC – Herói)"),
            ("superman", "Superman (DC – Herói)"),
            ("wonder_woman", "Mulher-Maravilha (DC – Heroína)"),
            ("flash", "Flash (DC – Herói)"),
            ("aquaman", "Aquaman (DC – Herói)"),
        ],
    ),
    (
        "DC - Vilões",
        [
            ("joker", "Coringa (DC – Vilão)"),
            ("lex_luthor", "Lex Luthor (DC – Vilão)"),
            ("harley_quinn", "Arlequina (DC – Vilã)"),
        ],
    ),
    (
        "Marvel - Heróis",
        [
            ("iron_man", "Homem de Ferro (Marvel – Herói)"),
            ("captain_america", "Capitão América (Marvel – Herói)"),
            ("thor", "Thor (Marvel – Herói)"),
            ("hulk", "Hulk (Marvel – Herói)"),
            ("spider_man", "Homem-Aranha (Marvel – Herói)"),
            ("black_widow", "Viúva Negra (Marvel – Heroína)"),
            ("black_panther", "Pantera Negra (Marvel – Herói)"),
        ],
    ),
    (
        "Marvel - Vilões",
        [
            ("thanos", "Thanos (Marvel – Vilão)"),
            ("loki", "Loki (Marvel – Vilão)"),
            ("ultron", "Ultron (Marvel – Vilão)"),
            ("green_goblin", "Duende Verde (Marvel – Vilão)"),
        ],
    ),
]

EXCEL_EXPERIENCE_CHOICES = [
    ("Iniciante", "Iniciante em Excel"),
    ("Intermediário", "Intermediário em Excel"),
    ("Avançado", "Avançado em Excel"),
]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    avatar_emoji = forms.ChoiceField(
        label="Escolha um avatar (emoji)",
        choices=[(e, e) for e in EMOJI_CHOICES],
        widget=forms.RadioSelect,
    )
    professional_profile = forms.ChoiceField(
        label="Qual perfil profissional mais se aproxima de você?",
        choices=UserProfile.ProfessionalProfile.choices,
    )
    favorite_character = forms.ChoiceField(
        label="Qual personagem (herói ou vilão) de DC/Marvel mais combina com você?",
        choices=HERO_VILLAIN_CHOICES,
        required=False,
    )
    excel_experience = forms.ChoiceField(
        label="Qual é o seu nível de experiência com Excel?",
        choices=EXCEL_EXPERIENCE_CHOICES,
        initial="Iniciante",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajusta textos dos campos padrão
        self.fields["username"].label = "Nome de usuário"
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirme a senha"

        # Aplica classes de estilo para inputs
        input_class = (
            "w-full border border-gray-300 rounded-md px-3 py-2 text-sm "
            "focus:outline-none focus:ring-2 focus:ring-emerald-500"
        )
        select_class = (
            "w-full border border-gray-300 rounded-md px-3 py-2 text-sm bg-white "
            "focus:outline-none focus:ring-2 focus:ring-emerald-500"
        )
        radio_class = "flex flex-wrap gap-2"

        for field in self.fields.values():
            widget = field.widget
            existing = widget.attrs.get("class", "")
            if isinstance(widget, forms.RadioSelect):
                base = radio_class
            elif isinstance(widget, forms.Select):
                base = select_class
            else:
                base = input_class
            widget.attrs["class"] = f"{existing} {base}".strip()

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

