from django import forms

from .models import Zlecenie


class ZlecenieForm(forms.ModelForm):
    class Meta:
        model = Zlecenie
        fields = [
            "tytul",
            "opis",
            "kategoria",
            "miasto",
            "dzielnica",
            "data_start",
            "czas_trwania_h",
            "stawka_h",
            "ok_dla_niepelnoletnich",
        ]

    def clean_stawka_h(self):
        value = self.cleaned_data["stawka_h"]
        if value > 40:
            raise forms.ValidationError("Stawka nie może przekraczać 40 PLN/h w wersji MVP.")
        return value


class ZlecenieFilterForm(forms.Form):
    miasto = forms.CharField(required=False)
    dzielnica = forms.CharField(required=False)
    tylko_dzis = forms.BooleanField(required=False)
    tylko_weekend = forms.BooleanField(required=False)
    max_czas = forms.BooleanField(required=False, label="Do 2h")
    max_stawka = forms.BooleanField(required=False, label="Do 40 zł/h")
    ok_dla_niepelnoletnich = forms.BooleanField(required=False)
