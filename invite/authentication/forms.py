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
    username = forms.CharField(
        min_length=2,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    first_name = forms.CharField(
        min_length=2,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Depan'}),
    )
    middle_name = forms.CharField(
        min_length=2,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Tengah'}),
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Belakang'}),
    )
    universitas = forms.CharField(
        min_length=2,
        max_length=40,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Universitas'}),
    )
    jurusan = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jurusan'}),
    )
    keahlian = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keahlian'}),
    )
    password1 = forms.CharField(
        min_length=8,
        max_length=26,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        min_length=8,
        max_length=26,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}),
    )
    class Meta:
        model = RegisteredUser
        fields = REGISTERED_USER_FIELDS

class RegisteredUserLoginFormNew(AuthenticationForm):
    pass

class RegisteredUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)

class RegisteredUserChangeForm(UserChangeForm):
    class Meta:
        model = RegisteredUser
        fields = REGISTERED_USER_FIELDS
