from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

EMOJI_CHOICES = ["🧠","🧮","📊","💹","🧑‍💻","🎯","🚀","🐍","📈","💼"]

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar_emoji = forms.ChoiceField(choices=[(e, e) for e in EMOJI_CHOICES])
    professional_profile = forms.ChoiceField(choices=UserProfile.ProfessionalProfile.choices)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar_emoji", "professional_profile")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email