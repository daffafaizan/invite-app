import datetime, logging
from django.conf import settings
from django.http import request, JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, FormView
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from authentication.models import RegisteredUser
from .forms import RegisteredUserCreationForm, RegisteredUserLoginForm
from .models import TautanMediaSosial, ProfileDetails, RegisteredUser

logger = logging.getLogger('app_api') # from settings.py

# NOTE reference: https://learndjango.com/tutorials/django-custom-user-model
class RegisterView(CreateView):
    form_class = RegisteredUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "authentication/register.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("core:home"))
        
        form = self.form_class()
        context = {
            "status": "Fetching form",
            "form": form,
        }

        return render(request, self.template_name, context, status=200)
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # Create user but don't save to db just yet
            user = form.save(commit=False)
            user.save()
            messages.success(request, f"Registered {user.username}!")

            return redirect(self.success_url)
        else:
            for error in form.errors:
                logger.error("FAILED, Form invalid")
                messages.error(request, error)
                return redirect(request.path)

class LoginView(FormView):
    form_class = RegisteredUserLoginForm
    success_url = reverse_lazy("core:home")
    template_name = "authentication/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("core:home"))
        
        form = self.form_class()
        context = {
            "status": "Fetching form",
            "form": form,
        }

        return render(request, self.template_name, context, status=200)

    def post(self, request):
        logger.info(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            use_email = False
            if "@" in form.cleaned_data["username_email"]:
                use_email = True

            if use_email:
                # Email auth
                user = authenticate(
                    username=form.cleaned_data["username_email"],
                    password=form.cleaned_data["password"]
                )
                
            else:
                # Username auth
                user = authenticate(
                    username=form.cleaned_data["username_email"],
                    password=form.cleaned_data["password"]
                )

            if user is not None:
                login(request, user)

                # Set cookies
                if use_email:
                    registered_user = RegisteredUser.objects.get(email=form.cleaned_data["username_email"])
                else:
                    registered_user = RegisteredUser.objects.get(username=form.cleaned_data["username_email"])

                logger.info(f"LOGGED IN AS {user.get_username()}")
                messages.success(request, f"Logged in as {user.username}!")

                res = redirect(reverse("core:home"))
                res.set_cookie("last_login", datetime.datetime.now())
                res.set_cookie("user_id", registered_user.id)

                return res
            else:
                context = {
                    "status": "Invalid username or password",
                    "form": form,
                }
                logger.error("USER:", user)   
                logger.error("LOGIN FAILED")
                messages.error(request, "Invalid username or password")

                return render(request, self.template_name, context, status=500)
        else:
            for error in form.errors:
                logger.error("FAILED, Form invalid")
                messages.error(request, error)
                return redirect(request.path)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("authentication:login"))
        
        logger.info("LOGGED OUT of %s" % request.user.get_username())
        logout(request)

        res = redirect(reverse("core:home"))
        res.delete_cookie("last_login")
        res.delete_cookie("user_id")

        return res
