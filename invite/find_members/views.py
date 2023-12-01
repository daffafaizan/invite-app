from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user_profile.models import KetuaRegu, RegisteredUser
from .forms import LowonganForm
from .models import *

@login_required(login_url='/accounts/login/')
def create_vacancy(request):

    form = LowonganForm()

    if request.method == 'POST':
        form = LowonganForm(request.POST)
        
        if form.is_valid():
            lowongan = form.save(commit=False)

            current_user = request.user
            current_pencari_regu = PencariRegu.objects.get(registered_user=current_user)
            ketua_regu = KetuaRegu(pencari_regu=current_pencari_regu)
            lowongan.ketua_regu = ketua_regu

            lowongan.nama_regu = request.POST.get('nama_regu')
            lowongan.deskripsi_lowongan_regu = request.POST.get('deskripsi_lowongan_regu')
            lowongan.foto_lowongan_regu = request.foto_lowongan_regu 

            lowongan.nama_lomba = request.nama_lomba
            lowongan.bidang_lomba = request.bidang_lomba
            lowongan.tanggal_lomba = request.tanggal_lomba 
            lowongan.expiry = request.expiry 
            
            lowongan.jumlah_anggota_sekarang = request.POST.get('jumlah_anggota_sekarang')
            lowongan.total_anggota_dibutuhkan = request.POST.get('total_anggota_dibutuhkan')
            
            tautan_medsos_regu = TautanMediaSosialLowongan(
                website = request.POST.get('website'),
                instagram = request.POST.get('instagram'),
                twitter = request.POST.get('twitter'),
                linkedin = request.POST.get('linkedin'), 
                github = request.POST.get('github'),
            )
            lowongan.tautan_medsos_regu = tautan_medsos_regu

            lowongan.save()

            # if succesful, return to melihat daftar lowongan and show created lowongan on top 
            return redirect('find_teams:apply')
        
    context = {
        'form': form
    }

    # if unsuccesful, reload form and display inputted values
    return render(request, 'create_vacancy.html', context)
