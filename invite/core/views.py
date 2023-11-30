from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def index(request):
    # Show main (index) page after logging in
    if request.user.is_authenticated:
        context = {
            "user": request.user,
        }
        return render(request, "core/index.html", context)
    else:
        return redirect(reverse("authentication:login"))