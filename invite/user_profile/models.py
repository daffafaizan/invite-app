from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

from authentication.models import RegisteredUser
from .models import PencariRegu

class ProfileDetails(models.Model):
    user = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
    jumlah_upvote = models.PositiveIntegerField(default=0)
    jumlah_downvote = models.PositiveIntegerField(default=0)

class UlasanProfil(models.Model):
    pengulas = models.OneToOneField(PencariRegu, on_delete=models.CASCADE, blank=False, null=False)
    diulas = models.OneToOneField(PencariRegu, on_delete=models.SET_NULL, blank=False, null=True) # Blank = False so form field should never be null, but db may contain null

    pengulas = models.ForeignKey(PencariRegu, on_delete=models.CASCADE, related_name='pengulas', blank=False, null=False)
    diulas = models.ForeignKey(PencariRegu, on_delete=models.SET_NULL, related_name='diulas', blank=False, null=True) # if NULL, then diulas is an Unknown User

    rating = models.PositiveIntegerField(default=0)
    deskripsi_kerja_setim = models.TextField() # NOTE user mengisi lomba apa yang pernah diikuti bersama user ini
    ulasan = models.TextField()

class PencariRegu(models.Model):
    user = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
    
    # # TODO admin 
    # dihapus_oleh = models.OneToOneField(Admin)

class KetuaRegu(models.Model):
    user = models.OneToOneField(PencariRegu, on_delete=models.CASCADE)

# # TODO admin
# class InviteAdmin(AbstractUser):
#     pengguna_dihapus = ArrayField(PencariRegu, blank=True, null=True) # Don't use arrayfield, use foreign key instead
    # lowongan_dihapus = ArrayField(Lowongan, blank=True, null=True)