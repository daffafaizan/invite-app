from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    path('me/', views.MyProfileDetailView.as_view(), name='me'),
    path('<str:user_id>/', views.ProfileDetailView.as_view(), name='profile'),
    path('my-applications/', views.show_my_applications, name='show_my_applications'),
    path('my-applications/<int:application_id>/delete', views.delete_application, name='delete_application'),
]