from django.contrib import admin
from django.urls import path, include
from tickets import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("tickets/", include("tickets.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
