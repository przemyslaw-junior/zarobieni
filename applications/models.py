from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from jobs.models import Zlecenie


class Zgloszenie(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Oczekujace"
        ACCEPTED = "accepted", "Zaakceptowane"
        REJECTED = "rejected", "Odrzucone"
        COMPLETED = "completed", "Zakonczone"

    zlecenie = models.ForeignKey(Zlecenie, on_delete=models.CASCADE, related_name="zgloszenia")
    wykonawca = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="zgloszenia")
    wiadomosc = models.TextField()
    proponowana_stawka = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="decided_applications",
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("zlecenie", "wykonawca")
        verbose_name = "Zgloszenie"
        verbose_name_plural = "Zgloszenia"

    def __str__(self):
        return f"{self.wykonawca} -> {self.zlecenie}"

    def clean(self):
        # Wspólna rola – każdy zalogowany może zgłaszać/udzielać pomocy.
        # Jeżeli wykonawca nie jest ustawiony (np. podczas is_valid przed nadpisaniem w widoku), pomijamy walidację.
        if not getattr(self, "wykonawca", None):
            return

    def get_absolute_url(self):
        return reverse("applications:detail", args=[self.pk])

    def accept(self, user):
        if user != self.zlecenie.owner:
            raise ValidationError("Tylko proszacy o pomoc moze zaakceptowac zgloszenie.")
        if self.status != self.Status.PENDING:
            raise ValidationError("Zgloszenie nie jest w stanie oczekujacym.")
        if not self.zlecenie.has_capacity:
            raise ValidationError("Zlecenie nie przyjmuje wiecej zgloszen.")
        self.status = self.Status.ACCEPTED
        self.decided_at = timezone.now()
        self.decided_by = user
        self.save(update_fields=["status", "decided_at", "decided_by"])
        self.zlecenie.mark_in_progress(self)

    def reject(self, user):
        if user != self.zlecenie.owner:
            raise ValidationError("Tylko proszacy o pomoc moze odrzucic zgloszenie.")
        if self.status != self.Status.PENDING:
            raise ValidationError("Zgloszenie nie jest w stanie oczekujacym.")
        self.status = self.Status.REJECTED
        self.decided_at = timezone.now()
        self.decided_by = user
        self.save(update_fields=["status", "decided_at", "decided_by"])

    def complete(self, user):
        if user != self.zlecenie.owner:
            raise ValidationError("Tylko proszacy o pomoc moze oznaczyc zakonczenie.")
        if self.status != self.Status.ACCEPTED:
            raise ValidationError("Zgloszenie nie jest aktywne.")
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at"])
        self.zlecenie.complete()

    @property
    def is_active(self):
        return self.status == self.Status.ACCEPTED
