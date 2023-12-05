# authentication/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import RegisteredUser

REGISTERED_USER_FIELDS = (
            "username", 
            "first_name", 
            "middle_name", 
            "last_name",
            "universitas",
            "jurusan",
            "keahlian",
            )

class RegisteredUserCreationForm(UserCreationForm):
    class Meta:
        model = RegisteredUser
        fields = REGISTERED_USER_FIELDS

class RegisteredUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)

class RegisteredUserChangeForm(UserChangeForm):
    class Meta:
        model = RegisteredUser
        fields = REGISTERED_USER_FIELDS
