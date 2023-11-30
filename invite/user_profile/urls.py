from django.urls import path
from user_profile.views import show_my_applications, delete_application, my_profile

app_name = "user_profile"

urlpatterns = [
    path('me', my_profile, name='my_profile'),
    path('my-applications/', show_my_applications, name='show_my_applications'),
    path('my-applications/<int:application_id>/delete', delete_application, name='delete_application'),
]