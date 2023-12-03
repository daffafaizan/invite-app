from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from authentication.models import RegisteredUser
from find_teams.forms import LamaranForm
from find_members.models import LowonganRegu

def show_vacancies(request):
    vacancy_list = LowonganRegu.objects.all()

    context = {
        "vacancy_list": vacancy_list,
    }

    return render(request, "show_vacancies.html", context)

def show_vacancy_details(request, lowongan_id):
    # TODO
    return render(request, "vacancy.html")

@login_required(login_url=settings.LOGIN_URL)
def apply_vacancy_first(request):
    initial = {
        "first_page_data": request.session.get("first_page_data", None)
    }
    if request.method == "POST":
        keahlian = request.POST.get("keahlian")
        cover_letter = request.POST.get("cover_letter")
        portofolio = request.POST.get("portofolio")

        request.session["first_page_data"] = {
            "keahlian": keahlian,
            "cover_letter": cover_letter,
            "portofolio": portofolio
        }

        return redirect("find_teams:apply_vacancy_second")
    
    context = {
        "form": initial
    }

    return render(request, "apply_vacancy_first.html", context)

@login_required(login_url=settings.LOGIN_URL)
def apply_vacancy_second(request, lowongan_id):
    first_page_data = request.session.get("first_page_data", None)

    if first_page_data is None:
        return redirect("find_teams:apply_vacancy_first", lowongan_id=lowongan_id)
    
    current_user = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))
    vacancy = LowonganRegu.objects.get(id=lowongan_id)
    keahlian = first_page_data.get("keahlian")
    cover_letter = first_page_data.get("cover_letter")
    portofolio = first_page_data.get("portofolio")

    user_data = {
        "nama": current_user.nama,
        "universitas": current_user.universitas,
        "jurusan": current_user.jurusan,
    }

    if request.method == "POST":
        form_data = {
            "keahlian": keahlian,
            "cover_letter": cover_letter,
            "portofolio": portofolio,
            "status": "Pending",
            "nama": request.POST.get("nama"),
            "universitas": request.POST.get("universitas"),
            "jurusan": request.POST.get("jurusan"),
            "pengirim": current_user.username,
            "penerima": vacancy.ketua,
            "lowongan": vacancy
        }
        form = LamaranForm(data=form_data)

        if form.is_valid():
            form.save()

            return render(request, "application_success.html", {"lamaran": form})
        
    else:
        form_data = {
            "nama": user_data["nama"],
            "universitas": user_data["universitas"],
            "jurusan": user_data["jurusan"],
        }
        form = LamaranForm(initial=form_data)

    context = {
        "form": form,
        "user_data": user_data,  # Pass the user data to the template
    }

    return render(request, "apply_vacancy_second.html", context)