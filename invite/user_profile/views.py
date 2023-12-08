import logging
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.db.models import Q
from user_profile.models import UlasanProfil
from find_teams.models import Lamaran
from find_members.models import LowonganRegu
from authentication.models import RegisteredUser, ProfileDetails, TautanMediaSosial
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

logger = logging.getLogger("app_api")


class MyProfileDetailView(LoginRequiredMixin, DetailView):
    model = RegisteredUser
    template_name = "user_profile/my_profile.html"

    def get(self, request):
        # If showing my profile, auto-retrieve my user id from cookies
        try:
            registered_user = get_object_or_404(RegisteredUser, id=request.COOKIES.get("user_id"))
            tms = get_object_or_404(TautanMediaSosial, id=registered_user.tautan_media_sosial.id)
            pd = get_object_or_404(ProfileDetails, id=registered_user.profile_details.id)

            context = {
                "status": "Success fetching my profile",
                "data": {
                    "user": registered_user,
                    "tms": tms,
                    "pd": pd,
                },
            }

            messages.success(request, "Success fetching user profile.")
            logger.info(f"Showing {registered_user.get_username()}'s profile")
            
            return render(request, self.template_name, context, status=200)
        except Http404 as error:
            logger.error("ProfileDetailError: Object not found: %s" % str(error))

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = RegisteredUser
    template_name = "user_profile/profile.html"

    def get(self, request, user_id):
        # If showing other's profile, retrieve user id url params
        logger.info(f"id from path: %s" % str(user_id))

        try:
            registered_user = get_object_or_404(RegisteredUser, id=user_id)
            tms = get_object_or_404(TautanMediaSosial, id=registered_user.tautan_media_sosial.id)
            pd = get_object_or_404(ProfileDetails, id=registered_user.profile_details.id)

            filtered_user = {
                "id": registered_user.id,
                "username": registered_user.username,
                "first_name": registered_user.first_name,
                "last_name": registered_user.last_name,
                "universitas": registered_user.universitas,
                "jurusan": registered_user.jurusan,
                "keahlian": registered_user.keahlian,
                "tautan_portfolio": registered_user.tautan_portfolio,
                "foto_profil": registered_user.foto_profil,
            }
            
            ulasan = UlasanProfil.objects.filter(diulas=registered_user)
            context = {
                "status": "Success fetching user profile",
                "data": {
                    "user": registered_user,
                    "tms": tms,
                    "pd": pd,
                    "ulasan": ulasan,
                },
            }

            messages.success(request, "Success fetching user profile.")
            logger.info(f"Showing {registered_user.get_username()}'s profile")

            return render(request, self.template_name, context, status=200)
        except Http404 as error:
            logger.error("ProfileDetailError: Object not found: %s" % str(error))

        # registered_user = get_object_or_404(RegisteredUser, id=user_id)

        # filtered_user = {
        #     "id": registered_user.id,
        #     "username": registered_user.username,
        #     "first_name": registered_user.first_name,
        #     "last_name": registered_user.last_name,
        #     "universitas": registered_user.universitas,
        #     "jurusan": registered_user.jurusan,
        #     "keahlian": registered_user.keahlian,
        #     "tautan_portfolio": registered_user.tautan_portfolio,
        #     "tautan_media_sosial": registered_user.tautan_media_sosial,
        #     "profile_details": registered_user.profile_details,
        #     "foto_profil": registered_user.foto_profil,
        # }

        # ulasan = UlasanProfil.objects.filter(diulas=registered_user)
        # # Return certain fields only
        # context = {
        #     "status": "Success fetching user profile",
        #     "data": {"user": filtered_user, "ulasan": ulasan},
        # }

        # logger.info(f"Showing {registered_user.get_username()}'s profile")
        # logger.info(f"Registered user: {registered_user}\n")

        # return render(request, self.template_name, context, status=200)


@login_required(login_url="/accounts/login/")
def review_profile(request, profile_id):
    diulas = RegisteredUser.objects.get(id=profile_id)
    pengulas = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))

    if diulas == pengulas:
        logger.info("Can't review for your own profile")
        messages.error(request, "Can't review for your own profile")
        return redirect("profile:profile", user_id=profile_id)
    
    if request.method == "POST":
        diulas = RegisteredUser.objects.get(id=profile_id)
        rating = request.POST.get("rating")
        deskripsi_kerja_setim = request.POST.get("deskripsi_kerja_setim")
        ulasan = request.POST.get("ulasan")

        pengulas = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))
        UlasanProfil.objects.create(
            diulas=diulas,
            pengulas=pengulas,
            rating=rating,
            deskripsi_kerja_setim=deskripsi_kerja_setim,
            ulasan=ulasan,
        )
        return redirect("profile:profile", user_id=profile_id)


@login_required(login_url="/accounts/login/")
def show_my_applications(request):
    registered_user = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))

    if not registered_user:
        context = {
            "status": "User not found",
        }

        logger.info("User not found")
        return render(request, "user_profile/my_applications.html", context, status=404)

    daftar_lamaran = Lamaran.objects.filter(pengirim=registered_user)

    if not daftar_lamaran:
        logger.info("Tidak ada lamaran ditemukan")
        return render(request, "user_profile/my_applications.html", status=404)

    context = {"status": "success", "data": {"daftar_lamaran": daftar_lamaran}}

    return render(request, "user_profile/my_applications.html", context, status=200)


@login_required(login_url="/accounts/login/")
def delete_application(request, application_id):
    lamaran = Lamaran.objects.get(id=application_id)

    context = {"id": application_id, "nama": lamaran.lowongan.nama_regu}

    if not lamaran:
        logger.info("Lamaran tidak ditemukan")
        return render(request, "vacancies.html", status=404)

    if request.method == "POST":
        lamaran.delete()
        return render(request, "user_profile/delete_success.html")

    return render(request, "user_profile/delete_confirmation.html", context)

@login_required(login_url="/accounts/login/")
def show_my_vacancies(request):
    query = request.GET.get('q', '')  
    sort_order = request.GET.get('sort', 'newest') 
    
    vacancy_list = LowonganRegu.objects.filter(ketua=request.user).order_by('-created_at')

    if query:
        vacancy_list = vacancy_list.filter(
            Q(nama_regu__icontains=query) | 
            Q(nama_lomba__icontains=query) | 
            Q(bidang_lomba__icontains=query)
        )

    if sort_order == 'oldest':
        vacancy_list = vacancy_list.order_by('created_at')
    else:  # Default to newest
        vacancy_list = vacancy_list.order_by('-created_at')

    current_user = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))

    context = {
        'vacancy_list': vacancy_list,
        'current_user': current_user,
        'query': query,
        'sort_order': sort_order
    }

    return render(request, "show_my_vacancies.html", context)


@login_required(login_url="/accounts/login/")
def delete_profile_review(request, profile_id, review_id):
    try:
        current_user = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))
        diulas = get_object_or_404(RegisteredUser, id=profile_id)
        review = get_object_or_404(UlasanProfil, id=review_id)
    except RegisteredUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect(
            "error_page", message="You do not have permission to delete this review."
        )
    except UlasanProfil.DoesNotExist:
        messages.error(request, "Review not found.")
        return redirect(
            "error_page", message="You do not have permission to delete this review."
        )

    if review.diulas != diulas:
        logger.info("You do not have permission to delete this review.")
        messages.error(request, "You do not have permission to delete this review.")
        return redirect("profile:profile", user_id=profile_id)

    if review.pengulas != current_user:
        logger.info("You do not have permission to delete this review.")
        messages.error(request, "You do not have permission to delete this review.")
        return redirect("profile:profile", user_id=profile_id)

    review.delete()
    logger.info("Review Successfully Deleted")
    messages.success(request, "Review successfully deleted.")

    return redirect("profile:profile", user_id=profile_id)


def error_page(request, message):
    return render(request, "error.html", {"message": message})
