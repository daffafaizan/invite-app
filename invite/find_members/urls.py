from django.urls import path
from find_members.views import *

app_name = 'find_members'

urlpatterns = [
    path('create/', create_lowongan, name='create_lowongan'),
    
]