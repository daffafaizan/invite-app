from typing import List
from django.db import models
from user_profile.models import KetuaRegu, PencariRegu, Admin

class LowonganRegu(models.Model):
    lowongan_regu_id = models.CharField(max_length=255, primary_key=True)
    ketua = models.ForeignKey(KetuaRegu, on_delete=models.CASCADE)
    nama_regu = models.CharField(max_length=255)
    deskripsi_lowongan_regu = models.TextField()
    nama_lomba = models.CharField(max_length=255)
    bidang_lomba = models.CharField(max_length=255)
    tanggal_lomba = models.DateTimeField()
    expiry = models.DateTimeField()
    jumlah_anggota_sekarang = models.IntegerField()
    total_anggota_dibutuhkan = models.IntegerField()
    pengirim = models.ForeignKey(PencariRegu, on_delete=models.CASCADE, blank=True)
    foto_lowongan_regu = models.CharField(max_length=255, blank=True)
    tautan_medsos_regu = models.CharField(max_length=255, blank=True)
    dihapusOleh = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()

class LowonganManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def lowongan_list(self) -> List[LowonganRegu]:
        return list(self.get_queryset())