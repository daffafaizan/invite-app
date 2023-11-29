from django.urls import path
from user_profile.views import delete_application

app_name = "user_profile"

urlpatterns = [
    path('my-applications/<int:application_id>/delete', delete_application, name='delete_application'),
]