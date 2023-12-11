from django.urls import path
from . import views
from find_teams import views as find_teams_views

app_name = "core"

urlpatterns = [
    path("", find_teams_views.show_vacancies, name="home"),
    path("404/", views.error_404, name="404"),
]