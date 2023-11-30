from django.urls import path
from . import views

app_name = "apply"

urlpatterns = [
    path("", views.apply_lowongan, name="apply"),
]