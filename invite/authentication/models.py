# authentication/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class TautanMediaSosial(models.Model):
    website = models.CharField(max_length=250, blank=True) # blank=True null=False, avoid redundant NULL and "" default values
    instagram = models.CharField(max_length=250, blank=True)
    twitter = models.CharField(max_length=250, blank=True)
    linkedin = models.CharField(max_length=250, blank=True)
    github = models.CharField(max_length=250, blank=True)
    
# Extend the default User model, don't use OneToOne relation
class RegisteredUser(AbstractUser):
    def default_profile_details(self):
        return ProfileDetails.objects.create()
    
    def user_directory_path(self, filename):
        # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'user_{self.user.username}/{filename}'

    def __str__(self) -> str:
        return self.username

    # User object contains username/email and password, also first_name and last_name
    
    # user = models.OneToOneField(User, on_delete=models.CASCADE)

    middle_name = models.CharField(max_length=30, blank=True, null=True)

    universitas = models.CharField(max_length=100, blank=True, null=True) 
    jurusan = models.CharField(max_length=100, blank=True, null=True)
    keahlian = ArrayField(models.CharField(max_length=30, blank=True, null=True), blank=True, null=True)
    
    foto_profil = models.ImageField(upload_to=user_directory_path) # FOR LATER USAGE see https://stackoverflow.com/questions/64592126/how-get-image-from-images-model-to-home-page-in-django
    tautan_media_sosial = models.OneToOneField(TautanMediaSosial, on_delete=models.SET_NULL, blank=True, null=True)
    tautan_portfolio = models.CharField(max_length=250, blank=True, null=True)

class ProfileDetails(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    jumlah_upvote = models.PositiveIntegerField(default=0)
    jumlah_downvote = models.PositiveIntegerField(default=0)
