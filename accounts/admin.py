from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar_emoji", "professional_profile")
    list_filter = ("professional_profile",)