from django.urls import path
from . import views

app_name = 'find_members'

urlpatterns = [
    path('<uuid:vacancy_id>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('create/', views.create_vacancy, name='create_vacancy'),
    path('update/<uuid:vacancy_id>/', views.VacancyUpdateView.as_view(), name='update_vacancy'),
    path('delete/<uuid:vacancy_id>/', views.VacancyDeleteView.as_view(), name='delete_vacancy'),
]