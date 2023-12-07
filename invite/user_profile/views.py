import logging
from django.conf import settings

from django.shortcuts import redirect, render
from django.shortcuts import render
from django.views.generic.detail import DetailView

from user_profile.models import UlasanProfil
from find_teams.models import Lamaran
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
            }

            logger.info("User not found")
            return render(request, self.template_name, context, status=404)
        
        context = {
            "status": "Success fetching my profile",
            "data": {
                "registered_user": registered_user
            }
        }

        logger.info(f"Showing {registered_user.get_username()}'s profile")
        logger.info(f"Registered user: {registered_user}\n")

        return render(request, self.template_name, context, status=200)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = RegisteredUser
    template_name = "user_profile/profile.html"

    def get(self, request, user_id):
        # If showing other's profile, retrieve user id url params        
        logger.info(f"id from path: %s"%str(user_id))
        
        registered_user = RegisteredUser.objects.get(id=user_id)
        
        if not registered_user:
            return render(request, self.template_name, status=404)
        
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
            "status": "Success fetching user profile",
            "data": {
                "registered_user": filtered_user
            }
        }

        logger.info(f"Showing {registered_user.get_username()}'s profile")
        logger.info(f"Registered user: {registered_user}\n")

        return render(request, self.template_name, context, status=200)
    
def show_review_profile(request, profile_id):
    diulas = RegisteredUser.objects.get(id=profile_id)
    reviews = UlasanProfil.objects.filter(diulas=diulas)

    if not reviews:
        return render(request, "review_profile.html", status=404)
    context = {
        "status": "Success fetching user review profile",
        "data": {
            "reviews": reviews
        } 
    }
    
    return render(request, "review_profile.html", context, status=200)
    
def review_profile(request, profile_id):
    if request.method == "POST":
        diulas = RegisteredUser.objects.get(id=profile_id)
        rating = request.POST.get("rating")
        deskripsi_kerja_setim = request.POST.get("deskripsi_kerja_setim")
        ulasan = request.POST.get("ulasan")
        
        pengulas = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))
        UlasanProfil.objects.create(diulas=diulas, pengulas=pengulas, rating=rating, deskripsi_kerja_setim=deskripsi_kerja_setim, ulasan=ulasan)
        
        return redirect('user_profile:profile', profile_id=profile_id)

def show_my_applications(request):
    user = RegisteredUser.objects.get(username=request.COOKIES.get("user_id"))
    registered_user = RegisteredUser.objects.get(user=user)
    daftar_lamaran = Lamaran.objects.filter(pengirim=registered_user)

    if not daftar_lamaran:
        logger.info("Tidak ada lamaran ditemukan")
        return render(request, "my_applications.html", status=404)

    context = {
        "status": "success",
        "data": {
            "daftar_lamaran": daftar_lamaran
        }
    }

    return render(request, "my_applications.html", context, status=200)

def delete_application(request, application_id):
    lamaran = Lamaran.objects.get(id=application_id)
    
    if not lamaran:
        logger.info("Lamaran tidak ditemukan")
        return render(request, "vacancies.html", status=404)
    
    lamaran.delete()

    context = {
        "status": "success",
        "message": "Lamaran berhasil dihapus"
    }

    return render(request, "vacancies.html", context, status=204)