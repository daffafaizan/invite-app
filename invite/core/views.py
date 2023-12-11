from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def home(request):
    # Show main (index) page after logging in
    context = {}
    if request.user.is_authenticated:
        context = {
            "user": request.user,
        }
        return render(request, "home.html", context)
    else:
        return redirect(reverse("authentication:login"))