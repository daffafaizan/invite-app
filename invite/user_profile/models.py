from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

from authentication.models import RegisteredUser

class PencariRegu(models.Model):
    user = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)

class KetuaRegu(models.Model):
    user = models.OneToOneField(PencariRegu, on_delete=models.CASCADE)

class UlasanProfil(models.Model):
    pengulas = models.OneToOneField(PencariRegu, on_delete=models.CASCADE, blank=False, null=False, related_name='pengulas')
    diulas = models.OneToOneField(PencariRegu, on_delete=models.SET_NULL, blank=False, null=True, related_name='diulas') # Blank = False so form field should never be null, but db may contain null

    rating = models.PositiveIntegerField(default=0)
    deskripsi_kerja_setim = models.TextField() # NOTE user mengisi lomba apa yang pernah diikuti bersama user ini
    ulasan = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
