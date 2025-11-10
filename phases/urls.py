from django.urls import path
from . import views

app_name = "phases"

urlpatterns = [
    path("fase1/", views.phase1_index, name="phase1_index"),
    path("fase1/<slug:slug>/", views.exercise_detail, name="exercise_detail"),
    path("api/exercise/<slug:slug>/", views.get_exercise_details_json, name="api_exercise_details"),
    path("fase2/", views.phase2_guide, name="phase2_guide"),
    path("fase3/", views.phase3_index, name="phase3_index"),
    path("fase4/", views.phase4_index, name="phase4_index"),
    path("fase5/", views.phase5_index, name="phase5_index"),
]
