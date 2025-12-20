from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from jobs.models import Zlecenie


class Zgloszenie(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_DECLINED = "declined"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Oczekujące"),
        (STATUS_ACCEPTED, "Zaakceptowane"),
        (STATUS_DECLINED, "Odrzucone"),
        (STATUS_CANCELLED, "Anulowane"),
    ]

    zlecenie = models.ForeignKey(Zlecenie, on_delete=models.CASCADE, related_name="zgloszenia")
    wykonawca = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="zgloszenia")
    wiadomosc = models.TextField()
    proponowana_stawka = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("zlecenie", "wykonawca")
        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"

    def __str__(self):
        return f"{self.wykonawca} -> {self.zlecenie}"

    def clean(self):
        if not self.wykonawca.is_worker:
            raise ValidationError("Tylko wykonawca może złożyć zgłoszenie.")

    def get_absolute_url(self):
        return reverse("applications:detail", args=[self.pk])

    def accept(self):
        self.status = self.STATUS_ACCEPTED
        self.save(update_fields=["status"])
        self.zlecenie.mark_in_progress(self)

    def decline(self):
        self.status = self.STATUS_DECLINED
        self.save(update_fields=["status"])

    def cancel(self):
        self.status = self.STATUS_CANCELLED
        self.save(update_fields=["status"])
