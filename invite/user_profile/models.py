import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, MaxLengthValidator

from authentication.models import RegisteredUser

class UlasanProfil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 

    pengulas = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, blank=False, null=False, related_name='%(class)s_pengulas')
    diulas = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, blank=False, null=True, related_name='%(class)s_pengulas') # Blank = False so form field should never be null, but db may contain null

    rating = models.PositiveIntegerField(default=0)
    deskripsi_kerja_setim = models.TextField(validators=[MinLengthValidator(3), MaxLengthValidator(1000)]) # NOTE user mengisi lomba apa yang pernah diikuti bersama user ini
    ulasan = models.TextField(validators=[MinLengthValidator(15), MaxLengthValidator(2000)])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
