from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Adiciona as URLs do app 'core' (home)
    path("", include("core.urls", namespace="core")),
    path("admin/", admin.site.urls),
    path("contas/", include("accounts.urls", namespace="accounts")),
    path("fases/", include("phases.urls", namespace="phases")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

