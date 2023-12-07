import uuid
from django.db import models
from authentication.models import RegisteredUser
from find_members.models import LowonganRegu

class Lamaran(models.Model):
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Pending', 'Pending'),
        ('Denied', 'Denied'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 

    pengirim = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, blank=True, null=False, related_name='%(class)s_pengirim')
    penerima = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, blank=True, related_name='%(class)s_penerima')
    lowongan = models.ForeignKey(LowonganRegu, on_delete=models.CASCADE, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    nama = models.CharField(max_length=255)
    universitas = models.CharField(max_length=255)
    jurusan = models.CharField(max_length=255)
    keahlian = models.CharField(max_length=255)
    cover_letter = models.TextField(blank=True)
    tautan_portofolio = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)