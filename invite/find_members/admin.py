from django.contrib import admin
from .models import LowonganRegu

@admin.register(LowonganRegu)
class LowonganReguAdmin(admin.ModelAdmin):
    model = LowonganRegu
    list_display = ["nama_regu", "deskripsi_lowongan_regu", "nama_lomba", "jumlah_anggota_sekarang", "total_anggota_dibutuhkan", "is_active", "created_at"]
