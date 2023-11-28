from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from user_profile import PencariRegu

class TautanMediaSosial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=250, blank=True) # blank=True null=False, avoid redundant NULL and "" default values
    instagram = models.CharField(max_length=250, blank=True)
    twitter = models.CharField(max_length=250, blank=True)
    linkedin = models.CharField(max_length=250, blank=True)
    github = models.CharField(max_length=250, blank=True)

class ProfileDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jumlah_upvote = models.PositiveIntegerField(default=0)
    jumlah_downvote = models.PositiveIntegerField(default=0)

class UlasanProfil(models.Model):
    # id --> auto generated
    pengulas = models.OneToOneField(PencariRegu, on_delete=models.CASCADE, blank=False, null=False)
    diulas = models.OneToOneField(PencariRegu, on_delete=models.SET_NULL, blank=False, null=True) # Blank = False so form field should never be null, but db may contain null

    pengulas = models.ForeignKey(PencariRegu, on_delete=models.CASCADE, related_name='pengulas', blank=False, null=False)
    diulas = models.ForeignKey(PencariRegu, on_delete=models.SET_NULL, related_name='diulas', blank=False, null=True) # if NULL, then diulas is an Unknown User

    rating = models.PositiveIntegerField(default=0)
    deskripsi_kerja_setim = models.TextField() # NOTE user mengisi lomba apa yang pernah diikuti bersama user ini
    ulasan = models.TextField()
    
class RegisteredUser(models.Model):
    def default_profile_details(self):
        return ProfileDetails.objects.create()
    
    def user_directory_path(self, filename):
        # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'user_{self.user.username}/{filename}'

    # User object contains username/email and password, also first_name and last_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=30, blank=True, null=True)

    universitas = models.CharField(max_length=100, blank=True, null=True) 
    jurusan = models.CharField(max_length=100, blank=True, null=True)
    keahlian = ArrayField(models.CharField(max_length=30, blank=True, null=True), blank=True, null=True)
    
    foto_profil = models.ImageField(upload_to=user_directory_path) # FOR LATER USAGE see https://stackoverflow.com/questions/64592126/how-get-image-from-images-model-to-home-page-in-django
    tautan_media_sosial = models.OneToOneField(TautanMediaSosial, on_delete=models.SET_NULL, blank=True, null=True)
    tautan_portfoilo = models.CharField(max_length=250, blank=True, null=True)
    profile_details = models.OneToOneField(ProfileDetails, default=default_profile_details, on_delete=models.SET_DEFAULT, blank=True, null=True)
    
