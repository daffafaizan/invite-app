from django.shortcuts import render

from authentication.models import RegisteredUser
from find_teams.forms import LamaranForm
from find_members.models import LowonganRegu

def show_vacancies(request):
    vacancy_list = LowonganRegu.objects.all()

    context = {
        'vacancy_list': vacancy_list,
    }

    return render(request, "show_vacancies.html", context)

def show_vacancy_details(request, lowongan_id):
    # TODO
    return render(request, "vacancy.html")

def apply_vacancy(request, lowongan_id):
    current_user = RegisteredUser.objects.get(username=request.COOKIES.get("username"))
    vacancy = LowonganRegu.objects.get(id=lowongan_id)

    if request.method == "POST":
        form = LamaranForm(request.POST)
        if form.is_valid():
            lamaran = form.save(commit=False)
            lamaran.status = "Pending"
            lamaran.pengirim = RegisteredUser.objects.get(user=current_user)
            lamaran.penerima = vacancy.ketua
            lamaran.lowongan = vacancy
            lamaran.save()

            return render(request, "application_success.html", {'lamaran': lamaran})
        
    else:
        form = LamaranForm()

    return render(request, "vacancy.html", {'form': form})