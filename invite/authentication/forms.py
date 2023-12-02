# authentication/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import RegisteredUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, ButtonHolder

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
    def __init__(self, *args, **kwargs):
        super(RegisteredUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('username', css_class='form-input h-8 w-32 mb-4 bg-black', placeholder='Username'),
            Field('first_name', css_class='form-input h-8 w-32 mb-4', placeholder='Nama Depan'),
            Field('middle_name', css_class='form-input h-8 w-32 mb-4', placeholder='Nama Tengah'),
            Field('last_name', css_class='form-input h-8 w-32 mb-4', placeholder='Nama Belakang'),
            Field('universitas', css_class='form-input h-8 w-32 mb-4', placeholder='Universitas'),
            Field('jurusan', css_class='form-input h-8 w-32 mb-4', placeholder='Jurusan'),
            Field('keahlian', css_class='form-input h-8 w-32 mb-4', placeholder='Keahlian'),
            Field('password1', css_class='form-input h-8 w-32 mb-4', placeholder='Password'),
            Field('password2', css_class='form-input h-8 w-32 mb-4', placeholder='Password Confirmation'),
            ButtonHolder(
                Submit('submit', 'Sign Up', css_class='your-custom-submit-button-class')
            )
        )

class RegisteredUserLoginFormNew(AuthenticationForm):
    pass

class RegisteredUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)

class RegisteredUserChangeForm(UserChangeForm):
    class Meta:
        model = RegisteredUser
        fields = REGISTERED_USER_FIELDS
