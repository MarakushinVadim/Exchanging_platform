from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import server_error

handler404 = 'config.views.pageNotFound'
handler500 = server_error

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ads.urls", namespace="ads")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
