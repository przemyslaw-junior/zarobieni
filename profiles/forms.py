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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            base_class = "form-control"
            if name == "dostepnosc":
                base_class = "form-select"
            if name == "ok_dla_niepelnoletnich":
                continue
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base_class}".strip()
            if name == "kategorie":
                field.widget.attrs["placeholder"] = "np. sprzątanie, zakupy, spacery"
            if name == "bio":
                field.widget.attrs.setdefault("rows", 4)
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
