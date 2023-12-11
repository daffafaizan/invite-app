import datetime
from typing import List
import uuid

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

def get_n_days_future(n=180):
    # Default is 6 months
    return datetime.datetime.now() + datetime.timedelta(days=n)

class TautanMediaSosialLowongan(models.Model):
    def __str__(self) -> str:
        res = f"\nWebsite id: {self.id}\n"
        options = ["website", "instagram", "twitter", "linkedin", "github"]
        values = (self.website, self.instagram, self.twitter, self.linkedin, self.github)

        for i in range(len(options)):
            res += f"{options[i]}: {values[i]}\n"
        
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

# NOTE reference: https://stackoverflow.com/questions/61104897/python-django-best-practice-for-request-user-in-class-based-views-and-queryset
class LowonganReguQuerySet(models.QuerySet):
    def owned_by_user(self, user):
        return self.filter(ketua=user)

class LowonganManager(models.Manager):
    def get_queryset(self):
        return LowonganReguQuerySet(self.model, using=self._db)

    # def lowongan_list(self) -> List[LowonganRegu]:
    #     return list(self.get_queryset())
    
    def owned_by_user(self, user):
        return self.get_queryset().owned_by_user(user)

class LowonganRegu(models.Model):
    def vacancy_directory_path(self, filename):
        # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'MEDIA_ROOT/lowongan_{self.pk}/{filename}'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    
    ketua = models.ForeignKey("authentication.RegisteredUser", on_delete=models.CASCADE)

    nama_regu = models.CharField(max_length=255, blank=False, null=False) # non-null
    deskripsi_lowongan_regu = models.TextField(blank=False, null=False, validators=[MinLengthValidator(3), MaxLengthValidator(2000)])
    foto_lowongan_regu = models.ImageField(blank=True, null=True, upload_to=vacancy_directory_path)

    nama_lomba = models.CharField(max_length=255)
    bidang_lomba = models.CharField(max_length=255)
    tanggal_lomba = models.DateTimeField(blank=True, null=True)
    expiry = models.DateTimeField(default=get_n_days_future) # By default, set expiry date to 6 months from creation date

    jumlah_anggota_sekarang = models.PositiveIntegerField(default=0)
    total_anggota_dibutuhkan = models.PositiveIntegerField(default=0)
    
    tautan_medsos_regu = models.OneToOneField(TautanMediaSosialLowongan, on_delete=models.SET_NULL, blank=True, null=True)
    
    objects = LowonganManager()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
