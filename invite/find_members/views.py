from typing import Any
from django.conf import settings
from django.db import models
from django.forms.models import BaseModelForm
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from find_teams.models import Lamaran

from .forms import LowonganForm
from .models import LowonganRegu, TautanMediaSosialLowongan

class VacancyDetailView(DetailView):
    model = LowonganRegu
    pk_url_kwarg = 'vacancy_id'
    template_name = "find_members/vacancy_detail.html"
    context_object_name = "vacancy"
    
    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        else:
            raise AttributeError("VacancyDetailView must be called with either an object pk or a slug.")
    
        try:
            return queryset.get()
        except queryset.model.DoesNotExist:
            res = render(self.request, "find_members/vacancy_detail.html", {"vacancy": None})
            res.status_code = 404
            return res
            # return HttpResponse("LowonganRegu matching query does not exist.", status=404)

class MyVacanciesDetailView(LoginRequiredMixin, ListView):
    model = LowonganRegu
    template_name = "find_members/my_vacancies.html"
    context_object_name = "vacancies"
    
    def get_queryset(self) -> QuerySet[Any]:
        # Return only the vacancies created by the current user
        return self.model.objects.owned_by_user(self.request.user)
        # return LowonganRegu.objects.filter(is_active=True, ketua=self.request.user)

@login_required(login_url=settings.LOGIN_URL)
def create_vacancy(request):

    form = LowonganForm()

    if request.method == 'POST':
        form = LowonganForm(request.POST)
        
        if form.is_valid():
            lowongan = form.save(commit=False)

            lowongan.ketua = request.user
            lowongan.is_active = True
            
            tautan_medsos_regu = TautanMediaSosialLowongan(
                website = request.POST.get('website'),
                instagram = request.POST.get('instagram'),
                twitter = request.POST.get('twitter'),
                linkedin = request.POST.get('linkedin'), 
                github = request.POST.get('github'),
            )
            tautan_medsos_regu.save()
            lowongan.tautan_medsos_regu = tautan_medsos_regu

            lowongan.save()

            # if succesful, redirect to melihat daftar lowongan
            messages.success(request, 'Form submitted successfully!')
            return redirect('find_teams:show_vacancies')
        
    context = {
        'form': form
    }

    # if unsuccesful, reload form and display inputted values
    for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

    return render(request, 'find_members/create_vacancy.html', context)

class VacancyUpdateView(LoginRequiredMixin, UpdateView):
    model = LowonganRegu
    pk_url_kwarg = 'vacancy_id'
    template_name = "find_members/update_vacancy.html"
    success_url = reverse_lazy("find_teams:show_vacancies")

    fields = [
        'nama_regu', 'deskripsi_lowongan_regu', 'foto_lowongan_regu',
        'nama_lomba', 'bidang_lomba', 'tanggal_lomba', 'expiry',
        'jumlah_anggota_sekarang', 'total_anggota_dibutuhkan',
        'tautan_medsos_regu',
        ]
    def get_object(self, queryset=None) -> LowonganRegu:
        return self.model.objects.get(ketua=self.request.user, uuid=self.kwargs["vacancy_id"])
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.ketua = self.request.user
        return super().form_valid(form)

    
class VacancyDeleteView(LoginRequiredMixin, DeleteView):
    model = LowonganRegu
    pk_url_kwarg = 'vacancy_id'
    template_name = "find_members/delete_vacancy.html"
    success_url = reverse_lazy("find_teams:show_vacancies")
    context_object_name = "vacancy"

    def get_object(self, queryset=None) -> LowonganRegu:
        return self.model.objects.get(ketua=self.request.user, uuid=self.kwargs["vacancy_id"])
    
    
def vacancy_applicants(request, vacancy_id):

    applicants = Lamaran.objects.filter(id=vacancy_id)
    print(applicants)

    context = {
        'applicants': reversed(applicants),
    }

    return render(request, "find_members/vacancy_applicants.html", context)


