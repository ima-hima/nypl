"""nyplsite URL Configuration"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("nypl_app/", include("nypl_app.urls")),
    path("admin/", admin.site.urls),
]
