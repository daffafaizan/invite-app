from django.urls import path
from . import views 

app_name = "profile"

urlpatterns = [
    path("me", views.my_profile, name="me")
]