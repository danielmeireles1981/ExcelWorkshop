from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phase", "created_at")
    list_filter = ("phase", "created_at")
    search_fields = ("user__username",)
