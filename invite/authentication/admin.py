from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisteredUserCreationForm, RegisteredUserChangeForm
from .models import RegisteredUser, ProfileDetails, TautanMediaSosial

@admin.register(RegisteredUser)
class RegisteredUserAdmin(UserAdmin):
    readonly_fields = ["get_tautan_medsos", "get_profile_details"]

    add_form = RegisteredUserCreationForm
    form = RegisteredUserChangeForm
    model = RegisteredUser
    list_display = [
                    "username", 
                    "email",
                    "first_name",
                    "last_name",
                    "is_active",
                    "created_at",
                    ]
    # Extend the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': (
                "middle_name", 
                "universitas",
                "jurusan",
                "keahlian",
                "foto_profil",
                "tautan_portfolio",
            )
        }),
        ("Custom Relations", {
            "fields": (
                "get_tautan_medsos",
                "get_profile_details",
            )
        })
    )

    def get_tautan_medsos(self, reguser):
        return reguser.tautan_media_sosial

    def get_profile_details(self, reguser):
        return reguser.profile_details

@admin.register(ProfileDetails)
class ProfileDetailsAdmin(admin.ModelAdmin):
    search_fields = ["id"]
    list_display = [
                    "id",
                    "jumlah_upvote",
                    "jumlah_downvote",
                    "is_active",
                    "created_at",
                    "updated_at",
                    ]

@admin.register(TautanMediaSosial)
class TautanMediaSosialAdmin(admin.ModelAdmin):
    search_fields = ["id"]
    list_display = [
                    "id",
                    "instagram",
                    "twitter",
                    "github",
                    "is_active",
                    "created_at",
                    "updated_at",
                    ]