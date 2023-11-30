from django.urls import path
from . import views

app_name = "recruit"

urlpatterns = [
    path("create", views.create_lowongan, name="create"),
]