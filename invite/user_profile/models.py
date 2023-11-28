from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

from authentication.models import RegisteredUser, UlasanProfil

class PencariRegu(models.Model):
    registered_user = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
    
    # TODO dihapus_oleh = models.OneToOneField(Admin)

class KetuaRegu(models.Model):
    registered_user = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)

# TODO
# class InviteAdmin(AbstractUser):
#     pengguna_dihapus = ArrayField(PencariRegu, blank=True, null=True) # Don't use arrayfield, use foreign key instead
    # lowongan_dihapus = ArrayField(Lowongan, blank=True, null=True)