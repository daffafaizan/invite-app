from os import path
from user_profile.views import show_profile


app_name = "user_profile"
urlpatterns = [
    path('', show_profile, name='show_profile')
]