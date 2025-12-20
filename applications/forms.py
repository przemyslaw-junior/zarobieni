from django import forms

from .models import Zgloszenie


class ZgloszenieForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ["wiadomosc", "proponowana_stawka"]
        widgets = {"wiadomosc": forms.Textarea(attrs={"rows": 3})}
