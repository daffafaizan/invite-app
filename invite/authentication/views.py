import datetime, logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import request, JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from authentication.models import RegisteredUser
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from .forms import RegisteredUserCreationForm, RegisteredUserLoginForm

logger = logging.getLogger('app_api') # from settings.py

class RegisterView(CreateView):
    form_class = RegisteredUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "authentication/register.html"

class LoginView(FormView):
    form_class = RegisteredUserLoginForm #
    success_url = reverse_lazy("core:home")
    template_name = "authentication/login.html"

    def get(self, request):
        form = self.form_class
        message = ''
        context = {
            "form": form,
            "message": message
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            
            logger.info("USER", user)

            if user is not None:
                login(request, user)
                return redirect(self.success_url)
            
        message = "Login failed!"
        context = {
            "form": form,
            "message": message,
        }

        logger.error("LOGIN FAILED")
        return render(request, self.template_name, context)

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if RegisteredUser.objects.get(username=username).exists():
            context = {
                "status": "error",
                "status_code": 409,
                "message": "Username already exists"
            }
            return render(request, "authentication/register.html", context)

        # Else, create user
        user = RegisteredUser.objects.create_user(username=username, password=password)

        if user is not None:
            user.save()

            context = {
                "status": "success",
                "status_code": 201,
                "message": "User created"
            }
        else:
            context = {
                "status": "error",
                "status_code": 500,
                "message": "Unknown error while creating user"
            }

        return render(
            request,
            "authentication/register.html",
            context
        )


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            if user.is_active: # Delete flag for users
                login(request, user)

                # Redirect to index page
                response = HttpResponseRedirect(reverse("core:index"))
                
                response.set_cookie(
                    "username",
                    username
                )

                response.set_cookie(
                    "last_login",
                    str(datetime.datetime.now())
                )

                return response
        else:
            context = {
                "status": "error",
                "status_code": 404,
                "message": "User does not exist."
                }
        
            return render(
                request,
                "authentication/login.html",
                context
            )
    
    return render(request, "authentication/login.html", {
        "status": "error",
        "status_code": 405,
        "message": "Method not allowed"
    })
        
def logout_user(request):
    logout(request)

    response = HttpResponseRedirect(
        reverse("core:home")
    )

    response.delete_cookie("username")
    response.delete_cookie("last_login")

    return response
    

