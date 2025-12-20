from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class ProfilWykonawcy(models.Model):
    AVAILABILITY_CHOICES = [
        ("weekdays", "Dni robocze"),
        ("weekend", "Weekend"),
        ("flex", "Elastyczna"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="worker_profile")
    stawka_h = models.DecimalField("Stawka za godzinę", max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    dostepnosc = models.CharField(max_length=16, choices=AVAILABILITY_CHOICES, default="flex")
    kategorie = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True)
    ok_dla_niepelnoletnich = models.BooleanField(default=False)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Profil {self.user.username}"

    class Meta:
        verbose_name = "Profil wykonawcy"
        verbose_name_plural = "Profile wykonawców"
