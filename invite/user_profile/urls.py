from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    path('me/', views.MyProfileDetailView.as_view(), name='me'),
    path('<uuid:user_id>/', views.ProfileDetailView.as_view(), name='profile'),
    path('<uuid:user_id>/review/create/', views.review_profile, name='review_profile'),
    path('my-applications/', views.show_my_applications, name='show_my_applications'),
    path('my-applications/<uuid:application_id>/delete', views.delete_application, name='delete_application'),
]