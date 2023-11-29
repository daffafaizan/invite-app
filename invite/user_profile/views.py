from django.shortcuts import get_object_or_404, redirect, render

from invite.user_profile.models import PencariRegu, UlasanProfil

# Create your views here.
def review_profile(request, profile_id):
    if request.method == "POST":
        diulas = get_object_or_404(PencariRegu, id = profile_id)
        rating = request.POST.get("rating")
        deskripsi_kerja_setim = request.POST.get("deskripsi_kerja_setim")
        ulasan = request.POST.get("ulasan")
        
        pengulas = request.user
        UlasanProfil.objects.create(diulas=diulas, pengulas=pengulas, rating=rating, deskripsi_kerja_setim=deskripsi_kerja_setim, ulasan=ulasan)
        
        return redirect('user_profile:show_profile', profile_id=profile_id)
