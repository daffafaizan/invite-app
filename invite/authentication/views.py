import datetime, logging
from django.conf import settings
from django.http import request, JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, FormView
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info("REGISTERED user", form.cleaned_data["username"][0])

            res = HttpResponseRedirect(self.success_url)
            res.status_code(200)

            return res
        else:
            message = "Login failed!"

            context = {
                "status": message,
                "form": form,
            }

            logger.error("FAILED, Form invalid")
            logger.error(form.errors)

            return render(request, self.template_name, context, status=500)

# TODO current form is still sent in plaintext, use LoginView in the future
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.views.LoginView
class LoginViewAuth(LoginView):
    template_name = "authentication/login.html"
    next_page = settings.LOGIN_REDIRECT_URL


class LoginViewOld(FormView):
    form_class = RegisteredUserLoginForm #
    success_url = reverse_lazy("core:home")
    template_name = "authentication/login.html"

    def get(self, request):
        form = self.form_class
        context = {
            "status": "Fetching form",
            "form": form,
        }

        return render(request, self.template_name, context, status=200)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user is not None:
                login(request, user)

                # Set cookies
                registered_user = RegisteredUser.objects.get(username=form.cleaned_data["username"])

                logger.info("LOGGED IN AS", user.get_username())

                res = HttpResponseRedirect(self.success_url)
                res.status_code(200)

                res.set_cookie("last_login", datetime.datetime.now())
                res.set_cookie("user_id", registered_user.id)

                return res
            
        context = {
            "status": "Login failed!",
            "form": form,
        }

        logger.error("LOGIN FAILED")
        return render(request, self.template_name, context, status=500)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        logger.info("LOGGED OUT of %s"%request.user.get_username())

        res = HttpResponseRedirect(reverse("core:home"))
        res.status_code = 200
        res.delete_cookie("last_login")
        res.delete_cookie("user_id")

        return res
    

