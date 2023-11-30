from django.shortcuts import render

from django.contrib.auth.models import User
from find_teams.models import Lamaran
from user_profile.models import PencariRegu
from authentication.models import RegisteredUser

def my_profile(request):
    pass

def show_my_applications(request):
    user = User.objects.get(username=request.COOKIES.get("username"))
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