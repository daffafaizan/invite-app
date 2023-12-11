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
    
def error_404(request):
    status_code = 500
    message = "Internal Server Error"
    
    if request.status_code == 404:
        status_code = 404
        message = "Not Found"
    elif request.status_code == 403:
        status_code = 403
        message = "Forbidden"
    
    context = {
        "status_code": status_code,
        "message": message,
    }
    return render(request, context, '404.html')