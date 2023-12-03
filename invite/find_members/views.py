from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LowonganForm
from .models import *

@login_required(login_url='/accounts/login/')
def create_vacancy(request):

    form = LowonganForm()

    if request.method == 'POST':
        form = LowonganForm(request.POST)
        
        if form.is_valid():
            lowongan = form.save(commit=False)

            lowongan.ketua = request.user
            lowongan.is_active = True

            lowongan.nama_regu = request.POST.get('nama_regu')
            lowongan.deskripsi_lowongan_regu = request.POST.get('deskripsi_lowongan_regu')
            lowongan.foto_lowongan_regu = request.POST.get('foto_lowongan_regu')

            lowongan.nama_lomba = request.POST.get('nama_lomba')
            lowongan.bidang_lomba = request.POST.get('bidang_lomba')
            lowongan.tanggal_lomba = request.POST.get('tanggal_lomba')
            lowongan.expiry = request.POST.get('expiry')

            lowongan.jumlah_anggota_sekarang = request.POST.get('jumlah_anggota_sekarang')
            lowongan.total_anggota_dibutuhkan = request.POST.get('total_anggota_dibutuhkan')
            
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

    return render(request, 'create_vacancy.html', context)
