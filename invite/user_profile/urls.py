from django.urls import path
from . import views #import show_my_applications, MyProfileDetailView, ProfileDetailView

app_name = "profile"

urlpatterns = [
    path('me/', views.MyProfileDetailView.as_view(), name='my_profile'),
    path('<str:username>/', views.ProfileDetailView.as_view(), name='profile'),
    path('my-applications/', views.show_my_applications, name='show_my_applications'),
]