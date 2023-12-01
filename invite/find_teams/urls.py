from django.urls import path
from find_teams.views import *

app_name = "find_teams"

urlpatterns = [
    path('', show_vacancies, name='show_vacancies'),
    path('<int:lowongan_id>/details', show_vacancy_details, name='show_vacancy_details'),
    path('<int:lowongan_id>/apply', apply_vacancy, name='apply_vacancy'),
    path('json/', vacancy_json, name='vacancy_json'),
]