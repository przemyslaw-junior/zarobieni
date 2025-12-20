from django import forms

from .models import Wiadomosc


class WiadomoscForm(forms.ModelForm):
    class Meta:
        model = Wiadomosc
        fields = ["tresc"]
        widgets = {"tresc": forms.Textarea(attrs={"rows": 3})}
