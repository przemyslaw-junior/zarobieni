from django import forms

from .models import ProfilWykonawcy


class ProfilWykonawcyForm(forms.ModelForm):
    kategorie = forms.CharField(
        label="Rodzaje prac",
        help_text="Wpisz kategorie rozdzielone przecinkami",
        required=False,
    )

    class Meta:
        model = ProfilWykonawcy
        fields = ["stawka_h", "dostepnosc", "kategorie", "bio", "ok_dla_niepelnoletnich"]

    def clean_kategorie(self):
        value = self.cleaned_data.get("kategorie", "")
        if not value:
            return []
        return [item.strip() for item in value.split(",") if item.strip()]

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.kategorie = self.cleaned_data.get("kategorie", [])
        if commit:
            profile.save()
        return profile
