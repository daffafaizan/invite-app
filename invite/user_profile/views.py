from django.shortcuts import get_object_or_404, render

from user_profile.models import PencariRegu, UlasanProfil

# Create your views here.
def show_profile(request, profile_id):
    diulas = get_object_or_404(PencariRegu, id=profile_id)
    
    reviews = UlasanProfil.objects.filter(diulas=diulas)
    context = {
        'profile': diulas,
        'reviews': reviews,
    }
    return render(request, "profile.html", context)