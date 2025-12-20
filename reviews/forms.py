from django import forms

from .models import Opinia


class OpiniaForm(forms.ModelForm):
    class Meta:
        model = Opinia
        fields = ["rating", "comment"]
        widgets = {"comment": forms.Textarea(attrs={"rows": 3})}
