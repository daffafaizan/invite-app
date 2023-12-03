from django.urls import path
from find_teams.views import show_vacancies, show_vacancy_details, apply_vacancy

app_name = "find_teams"

urlpatterns = [
    path('', show_vacancies, name='show_vacancies'),
    path('<uuid:lowongan_id>/details', show_vacancy_details, name='show_vacancy_details'),
    path('<uuid:lowongan_id>/apply', apply_vacancy, name='apply_vacancy'),
]