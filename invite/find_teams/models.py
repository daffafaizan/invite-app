from django.db import models
from user_profile.models import PencariRegu, KetuaRegu
from find_members.models import LowonganRegu

class Lamaran(models.Model):
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Pending', 'Pending'),
        ('Denied', 'Denied'),
    ]

    lamaran_id = models.CharField(max_length=255, primary_key=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    nama = models.CharField(max_length=255)
    universitas = models.CharField(max_length=255)
    jurusan = models.CharField(max_length=255)
    keahlian = models.CharField(max_length=255)
    cover_letter = models.TextField(blank=True)
    tautan_portofolio = models.CharField(max_length=255)
    pengirim = models.ForeignKey(PencariRegu, on_delete=models.CASCADE, blank=True)
    penerima = models.ForeignKey(KetuaRegu, on_delete=models.CASCADE, blank=True)
    lowongan = models.ForeignKey(LowonganRegu, on_delete=models.CASCADE, blank=True)