import datetime, logging
from django.forms.models import BaseModelForm
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
            registered_user = form.save(commit=False)

            # pd = ProfileDetails.objects.create()
            # tms = TautanMediaSosial.objects.create()
            
            # form.instance.profile_details = pd
            # form.instance.tautan_media_sosial = tms
            
            # # Save all 3 objects
            # logger.info("pd", pd)
            # logger.info("tms", tms)

            # pd.save()
            # tms.save()

            registered_user.save()
            logger.info("REGISTERED user", form.cleaned_data["username"][0])

            return redirect(self.success_url)
        else:
            message = "Login failed!"
            context = {
                "form": form,
                "status_code": 500,
                "message": message,
            }

            logger.error("FAILED, Form invalid")
            logger.error(form.errors)
            return render(request, self.template_name, context)

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
            
            logger.info("LOGGED IN AS", user.get_username())

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
        logger.info("LOGGED OUT of %s"%request.user.get_username())
        return redirect(reverse("core:home"))
    

