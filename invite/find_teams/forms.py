# forms.py
from django import forms
from .models import Lamaran

class LamaranForm(forms.ModelForm):
    class Meta:
        model = Lamaran
        fields = ['nama', 'universitas', 'jurusan', 'keahlian', 'cover_letter', 'tautan_portofolio']
