# authentication/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import RegisteredUser

REGISTERED_USER_FIELDS = (
            "username", 
            "first_name", 
            "middle_name", 
            "last_name",
            "universitas",
            "jurusan",
            "keahlian",
            "foto_profil",
            "tautan_media_sosial",
            "tautan_portfolio"
            )

class RegisteredUserCreationForm(UserCreationForm):
    class Meta:
        model = RegisteredUser
        fields = REGISTERED_USER_FIELDS

class RegisteredUserChangeForm(UserChangeForm):
    class Meta:
        model = RegisteredUser
        fields = REGISTERED_USER_FIELDS
