import datetime, logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import request, JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from authentication.models import RegisteredUser
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views import View
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
            "status_code": 200,
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
            "status_code": 500,
            "message": message,
        }

        logger.error("LOGIN FAILED")
        return render(request, self.template_name, context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("core:home"))
    

