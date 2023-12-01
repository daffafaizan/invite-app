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

        
        context = {
            "registered_user": registered_user
        }

        logger.info(f"Showing {registered_user.get_username()}'s profile")
        logger.info(f"Registered user: {registered_user}\n")

        return render(request, self.template_name, context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = RegisteredUser
    template_name = "user_profile/profile.html"

    def get(self, request, user_id):
        # If showing other's profile, retrieve user id url params        
        logger.info("Uname path:", user_id)
        
        registered_user = RegisteredUser.objects \
            .filter(id=user_id) \
            .only(
                "username", 
                "first_name", 
                "last_name", 
                "universitas", 
                "jurusan", 
                "keahlian", 
                "tautan_portfolio", 
                "tautan_media_sosial", 
                "profile_details", 
                "foto_profil"
            ).get()

        context = {
            "registered_user": registered_user
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
        "daftar_lamaran": daftar_lamaran
    }

    return render(request, "my_applications.html", context)

def delete_application(request, application_id):
    lamaran = Lamaran.objects.get(id=application_id)
    lamaran.delete()

    return render(request, "vacancies.html")