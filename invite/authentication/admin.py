from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisteredUserCreationForm, RegisteredUserChangeForm
from .models import RegisteredUser

class RegisteredUserAdmin(UserAdmin):
    add_form = RegisteredUserCreationForm
    form = RegisteredUserChangeForm
    model = RegisteredUser
    list_display = [
                    "username", 
                    "first_name",
                    "last_name",
                    ]

admin.site.register(RegisteredUser, RegisteredUserAdmin)