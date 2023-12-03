from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from find_members.models import LowonganRegu

class LowonganForm(ModelForm):
    class Meta:
        model = LowonganRegu
        fields = ['nama_regu', 'deskripsi_lowongan_regu', 'foto_lowongan_regu',
                  'nama_lomba', 'bidang_lomba', 'tanggal_lomba', 'expiry',
                  'jumlah_anggota_sekarang', 'total_anggota_dibutuhkan',
                  'website', 'instagram', 'twitter', 'linkedin', 'github']

    foto_lowongan_regu = forms.ImageField(required=False)
    website = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    twitter = forms.CharField(required=False)
    linkedin = forms.CharField(required=False)
    github = forms.CharField(required=False)

    # validations

    # a minimum of 1 member (the team leader) is already in the team 
    jumlah_anggota_sekarang = forms.IntegerField(min_value=1, max_value=100)

    # a minimum of 1 needed member for a vacancy to exist
    total_anggota_dibutuhkan = forms.IntegerField(min_value=1, max_value=100)

    # competition date and vacancy expiry date cannot be before the current time
    tanggal_lomba = forms.DateTimeField(
        validators=[],
        widget=forms.TextInput(attrs={'type': 'datetime-local'})
    )
    expiry = forms.DateTimeField(
        validators=[],
        widget=forms.TextInput(attrs={'type': 'datetime-local'})
    )

    def clean_tanggal_lomba(self):
        tanggal_lomba = self.cleaned_data.get('tanggal_lomba')
        if tanggal_lomba and tanggal_lomba < timezone.now():
            raise ValidationError("Competition date cannot be before the current time.")
        return tanggal_lomba

    def clean_expiry(self):
        expiry = self.cleaned_data.get('expiry')
        if expiry and expiry < timezone.now():
            raise ValidationError("Expiry date cannot be before the current time.")
        return expiry

    def clean(self):
        cleaned_data = super().clean()
        jumlah_anggota_sekarang = cleaned_data.get('jumlah_anggota_sekarang')
        total_anggota_dibutuhkan = cleaned_data.get('total_anggota_dibutuhkan')

        if jumlah_anggota_sekarang is not None and total_anggota_dibutuhkan is not None:
            if total_anggota_dibutuhkan <= jumlah_anggota_sekarang:
                raise ValidationError("Total members needed must be greater than current members.")
        return cleaned_data