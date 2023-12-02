# authentication/models.py
import datetime, uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class TautanMediaSosial(models.Model):
    def __str__(self) -> str:
        res = "\nWebsites:\n"

        for link in (self.website, self.instagram, self.twitter, self.linkedin, self.github):
            res += f"{link}\n"
        
        return res
            
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
 
    website = models.CharField(max_length=250, blank=True) # blank=True null=False, avoid redundant NULL and "" default values
    instagram = models.CharField(max_length=250, blank=True)
    twitter = models.CharField(max_length=250, blank=True)
    linkedin = models.CharField(max_length=250, blank=True)
    github = models.CharField(max_length=250, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProfileDetails(models.Model):
    def __str__(self) -> str:
        res = "\nProfile details:\n"
        res += f"Upvote: {self.jumlah_upvote}\n"
        res += f"Downvote: {self.jumlah_downvote}\n"
        return res
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    
    jumlah_upvote = models.PositiveIntegerField(default=0)
    jumlah_downvote = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# Extend the default User model, don't use OneToOne relation
class RegisteredUser(AbstractUser):
    def user_directory_path(self, filename):
        # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'user_{self.user.username}/{filename}'

    def save(self, *args, **kwargs):
        # Check if profile_details is not set, then create a default ProfileDetails instance
        if not self.profile_details:
            default_pd = ProfileDetails.objects.create()
            self.profile_details = default_pd
        if not self.tautan_media_sosial:
            default_tms = TautanMediaSosial.objects.create()
            self.tautan_media_sosial = default_tms
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username

    # NOTE MODEL FIELDS
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 

    middle_name = models.CharField(max_length=30, blank=True)
    universitas = models.CharField(max_length=100, blank=True) 
    jurusan = models.CharField(max_length=100, blank=True)
    keahlian = ArrayField(models.CharField(max_length=30, blank=True), blank=True, null=True)
    
    foto_profil = models.ImageField(upload_to=user_directory_path) # FOR LATER USAGE see https://stackoverflow.com/questions/64592126/how-get-image-from-images-model-to-home-page-in-django
    tautan_portfolio = models.CharField(max_length=250, blank=True)

    tautan_media_sosial = models.OneToOneField(TautanMediaSosial, on_delete=models.SET_NULL, blank=True, null=True)
    profile_details = models.OneToOneField(ProfileDetails, on_delete=models.SET_NULL, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)