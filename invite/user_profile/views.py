import logging
from django.conf import settings

from django.shortcuts import render
from django.views.generic.detail import DetailView

from find_teams.models import Lamaran
from user_profile.models import PencariRegu
from authentication.models import RegisteredUser
from django.contrib.auth.decorators import login_required

logger = logging.getLogger("app_api")

class MyProfileDetailView(DetailView):
    login_required = True

    model = RegisteredUser
    template_name = "user_profile/my_profile.html"

    def get(self, request):
        # If showing my profile, auto-retrieve my user id from cookies
        registered_user = RegisteredUser.objects.get(username=request.COOKIES.get("username"))

        
        context = {
            "registered_user": registered_user
        }

        logger.info("Showing %s's profile" % registered_user.get_username())
        return render(request, self.template_name, context)

class ProfileDetailView(DetailView):
    login_required = True

    model = RegisteredUser
    template_name = "user_profile/profile.html"

    def get(self, request, username):
        # If showing other's profile, retrieve user id url params        
        logger.info("Uname path:", username)
        
        registered_user = RegisteredUser.objects.get(username=username)
        

        context = {
            "registered_user": registered_user
        }

        logger.info("Showing %s's profile" % registered_user.get_username())
        return render(request, self.template_name, context)


def show_my_applications(request):
    user = RegisteredUser.objects.get(username=request.COOKIES.get("username"))
    registered_user = RegisteredUser.objects.get(user=user)
    pencari_regu = PencariRegu.objects.get(user=registered_user)

    daftar_lamaran = Lamaran.objects.filter(pengirim=pencari_regu)

    context = {
        "daftar_lamaran": daftar_lamaran
    }

    return render(request, "my_applications.html", context)