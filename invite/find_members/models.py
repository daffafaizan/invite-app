import datetime
from typing import List
import uuid
from django.db import models
from authentication.models import RegisteredUser
from django.db import models

def get_n_days_future(n=180):
    # Default is 6 months
    return datetime.datetime.now() + datetime.timedelta(days=n)

class TautanMediaSosialLowongan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 

    website = models.CharField(max_length=250, blank=True) # blank=True null=False, avoid redundant NULL and "" default values
    instagram = models.CharField(max_length=250, blank=True)
    twitter = models.CharField(max_length=250, blank=True)
    linkedin = models.CharField(max_length=250, blank=True)
    github = models.CharField(max_length=250, blank=True)

class LowonganRegu(models.Model):
    def vacancy_directory_path(self, filename):
        # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'lowongan_{self.pk}/{filename}'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    
    ketua = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    nama_regu = models.CharField(max_length=255, blank=False, null=False) # non-null
    deskripsi_lowongan_regu = models.TextField()
    foto_lowongan_regu = models.ImageField(upload_to=vacancy_directory_path)

    nama_lomba = models.CharField(max_length=255)
    bidang_lomba = models.CharField(max_length=255)
    tanggal_lomba = models.DateTimeField()
    expiry = models.DateTimeField(default=get_n_days_future) # By default, set expiry date to 6 months from creation date

    jumlah_anggota_sekarang = models.PositiveIntegerField(default=0)
    total_anggota_dibutuhkan = models.PositiveIntegerField(default=0)
    
    tautan_medsos_regu = models.OneToOneField(TautanMediaSosialLowongan, on_delete=models.SET_NULL, blank=True, null=True)
    objects = models.Manager()

class LowonganManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def lowongan_list(self) -> List[LowonganRegu]:
        return list(self.get_queryset())