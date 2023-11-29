from django.urls import path
from user_profile.views import review_profile

app_name = "user_profile"
urlpatterns = [
    path('<int:profile_id>/review/create/', review_profile, name='review_profile'),
]
