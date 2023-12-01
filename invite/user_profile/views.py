import logging
from django.conf import settings

from django.shortcuts import render
from django.views.generic.detail import DetailView

from find_teams.models import Lamaran
from user_profile.models import PencariRegu
from authentication.models import RegisteredUser
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger("app_api")

class MyProfileDetailView(LoginRequiredMixin, DetailView):
    model = RegisteredUser
    template_name = "user_profile/my_profile.html"

    def get(self, request):
        # If showing my profile, auto-retrieve my user id from cookies
        registered_user = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))

        if not registered_user:
            context = {
                "status": "User not found",
                "status_code": 404,
            }

            logger.info("User not found")
            return render(request, self.template_name, context)
        
        context = {
            "status": "success",
            "status_code": 200,
            "data": {
                "registered_user": registered_user
            }
        }

        logger.info(f"Showing {registered_user.get_username()}'s profile")
        logger.info(f"Registered user: {registered_user}\n")

        return render(request, self.template_name, context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = RegisteredUser
    template_name = "user_profile/profile.html"

    def get(self, request, user_id):
        # If showing other's profile, retrieve user id url params        
        logger.info(f"id from path: %s"%str(user_id))
        
        registered_user = RegisteredUser.objects.get(id=user_id)
        
        if not registered_user:
            context = {
                
            }
            return render(request, self.template_name, context)
        filtered_user = {
            "id": registered_user.id,
            "username": registered_user.username,
            "first_name": registered_user.first_name,
            "last_name": registered_user.last_name,
            "universitas": registered_user.universitas,
            "jurusan": registered_user.jurusan,
            "keahlian": registered_user.keahlian,
            "tautan_portfolio": registered_user.tautan_portfolio,
            "tautan_media_sosial": registered_user.tautan_media_sosial,
            "profile_details": registered_user.profile_details,
            "foto_profil": registered_user.foto_profil,
        }

        # Return certain fields only
        context = {
            "status": "success",
            "status_code": 200,
            "data": {
                "registered_user": filtered_user
            }
        }

        logger.info(f"Showing {registered_user.get_username()}'s profile")
        logger.info(f"Registered user: {registered_user}\n")

        return render(request, self.template_name, context)


def show_my_applications(request):
    user = RegisteredUser.objects.get(username=request.COOKIES.get("user_id"))
    registered_user = RegisteredUser.objects.get(user=user)
    pencari_regu = PencariRegu.objects.get(user=registered_user)

    daftar_lamaran = Lamaran.objects.filter(pengirim=pencari_regu)

    context = {
        "status": "success",
        "status_code": 200,
        "data": {
            "daftar_lamaran": daftar_lamaran
        }
    }

    return render(request, "my_applications.html", context)

def delete_application(request, application_id):
    lamaran = Lamaran.objects.get(id=application_id)
    lamaran.delete()

    context = {
        "status": "success",
        "status_code": 204,
        "message": "Lamaran berhasil dihapus"
    }

    return render(request, "vacancies.html", context)