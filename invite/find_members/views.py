from django.shortcuts import render, redirect
from .forms import LowonganForm
from .models import TautanMediaSosialLowongan

def create_lowongan(request):

    form = LowonganForm()

    if request.method == 'POST':
        form = LowonganForm(request.POST)
        
        if form.is_valid():
            model_instance = form.save(commit=False)

            model_instance.ketua = request.user

            model_instance.nama_regu = request.POST.get('nama_regu')
            model_instance.deskripsi_lowongan_regu = request.POST.get('deskripsi_lowongan_regu')
            model_instance.foto_lowongan_regu = request.foto_lowongan_regu 

            model_instance.nama_lomba = request.nama_lomba
            model_instance.bidang_lomba = request.bidang_lomba
            model_instance.tanggal_lomba = request.tanggal_lomba 
            model_instance.expiry = request.expiry 
            
            model_instance.jumlah_anggota_sekarang = request.POST.get('jumlah_anggota_sekarang')
            model_instance.total_anggota_dibutuhkan = request.POST.get('total_anggota_dibutuhkan')
            
            tautan_medsos_regu = TautanMediaSosialLowongan(
                website = request.POST.get('website'),
                instagram = request.POST.get('instagram'),
                twitter = request.POST.get('twitter'),
                linkedin = request.POST.get('linkedin'), 
                github = request.POST.get('github'),
            )
            model_instance.tautan_medsos_regu = tautan_medsos_regu

            model_instance.save()

            # if succesful, return to melihat daftar lowongan and show created lowongan on top 
            return redirect('find_teams:apply')
        
    context = {
        'form': form
    }

    # if unsuccesful, reload form and display inputted values
    return render(request, 'create_lowongan.html', context)
