from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from jobs.models import Zlecenie


class Opinia(models.Model):
    zlecenie = models.ForeignKey(Zlecenie, on_delete=models.CASCADE, related_name="opinie")
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wystawione_opinie"
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otrzymane_opinie"
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Opinia"
        verbose_name_plural = "Opinie"
        unique_together = ("zlecenie", "reviewer")

    def __str__(self):
        return f"Opinia {self.reviewee} ({self.rating})"

    def get_absolute_url(self):
        return reverse("reviews:detail", args=[self.pk])
