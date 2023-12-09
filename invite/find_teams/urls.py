from django.urls import path
from . import views

app_name = "find_teams"

urlpatterns = [
    path('', views.show_vacancies, name='show_vacancies'),
    path('<uuid:lowongan_id>/apply/first', views.apply_vacancy_first, name='apply_vacancy_first'),
    path('<uuid:lowongan_id>/apply/second', views.apply_vacancy_second, name='apply_vacancy_second'),
    path('bookmark', views.show_bookmarked, name='show_bookmarked')
]