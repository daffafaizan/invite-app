from django.urls import path
from . import views
from find_teams import views as find_teams_views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    # path("", find_teams_views.show_vacancies, name="home"),
]