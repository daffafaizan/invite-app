import logging
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Q
from authentication.models import RegisteredUser
from find_teams.forms import LamaranForm
from find_members.models import LowonganRegu, TautanMediaSosialLowongan

logger = logging.getLogger("app_api")


@login_required(login_url="/accounts/login/")
def show_vacancies(request):
    query = request.GET.get("q", "")
    sort_order = request.GET.get("sort", "newest")

    vacancy_list = LowonganRegu.objects.all()

    if query:
        vacancy_list = vacancy_list.filter(
            Q(nama_regu__icontains=query)
            | Q(nama_lomba__icontains=query)
            | Q(bidang_lomba__icontains=query)
        )

    if sort_order == "oldest":
        vacancy_list = vacancy_list.order_by("created_at")
    else:  # Default to newest
        vacancy_list = vacancy_list.order_by("-created_at")

    current_user = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))

    context = {
        "vacancy_list": vacancy_list,
        "current_user": current_user,
        "query": query,
        "sort_order": sort_order,
    }

    return render(request, "show_vacancies.html", context)


def show_vacancy_details(request, lowongan_id):
    context = {
        "vacancy": False,
        "sosmed": False,  # Pass the user data to the template
    }
    try:
        vacancy = LowonganRegu.objects.get(id=lowongan_id)
        context["vacancy"] = vacancy
    except (LowonganRegu.DoesNotExist, ValueError):
        return render(request, "show_vacancy_details.html", context)

    try:
        sosmed = vacancy.tautan_medsos_regu
        context["sosmed"] = sosmed
    except (LowonganRegu.DoesNotExist, ValueError):
        return render(request, "show_vacancy_details.html", context)

    return render(request, "show_vacancy_details.html", context)


@login_required(login_url=settings.LOGIN_URL)
def apply_vacancy_first(request, lowongan_id):
    initial = {"first_page_data": request.session.get("first_page_data", None)}

    current_user = RegisteredUser.objects.get(id=request.COOKIES.get("user_id"))
    penerima = LowonganRegu.objects.get(id=lowongan_id).ketua

    if current_user == penerima:
        logger.info("Can't apply to your own vacancy")

        return redirect("find_teams:show_vacancies")

    if request.method == "POST":
        keahlian = request.POST.get("keahlian")
        cover_letter = request.POST.get("cover_letter")
        tautan_portofolio = request.POST.get("tautan_portofolio")

        request.session["first_page_data"] = {
            "keahlian": keahlian,
            "cover_letter": cover_letter,
            "tautan_portofolio": tautan_portofolio,
        }

        return redirect("find_teams:apply_vacancy_second", lowongan_id=lowongan_id)

    context = {"form": initial, "vacancy": LowonganRegu.objects.get(id=lowongan_id)}

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
    tautan_portofolio = first_page_data.get("tautan_portofolio")

    user_data = {
        "nama": current_user.first_name,
        "universitas": current_user.universitas,
        "jurusan": current_user.jurusan,
    }

    if request.method == "POST":
        form_data = {
            "keahlian": keahlian,
            "cover_letter": cover_letter,
            "tautan_portofolio": tautan_portofolio,
            "nama": request.POST.get("nama"),
            "universitas": request.POST.get("universitas"),
            "jurusan": request.POST.get("jurusan"),
        }

        form = LamaranForm(data=form_data)
        print(form_data)

        if form.is_valid():
            lamaran = form.save(commit=False)
            lamaran.pengirim = current_user
            lamaran.penerima = vacancy.ketua
            lamaran.lowongan = vacancy
            lamaran.status = "Pending"
            lamaran.save()

            return render(request, "application_success.html")

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
