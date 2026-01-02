from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Zlecenie(models.Model):
    STATUS_PUBLISHED = "published"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PUBLISHED, "Opublikowane"),
        (STATUS_IN_PROGRESS, "W trakcie"),
        (STATUS_COMPLETED, "Zakończone"),
        (STATUS_CANCELLED, "Anulowane"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="zlecenia")
    tytul = models.CharField(max_length=120)
    opis = models.TextField()
    kategoria = models.CharField(max_length=64)
    miasto = models.CharField(max_length=64)
    dzielnica = models.CharField(max_length=64, blank=True)
    data_start = models.DateField()
    czas_trwania_h = models.PositiveIntegerField(validators=[MaxValueValidator(2)])
    stawka_h = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    ok_dla_niepelnoletnich = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PUBLISHED)
    helpers_needed = models.PositiveIntegerField(default=1)
    accepted_application = models.ForeignKey(
        "applications.Zgloszenie", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Zlecenie"
        verbose_name_plural = "Zlecenia"

    def __str__(self):
        return self.tytul

    def get_absolute_url(self):
        return reverse("jobs:detail", args=[self.pk])

    def publish(self):
        self.status = self.STATUS_PUBLISHED
        self.save(update_fields=["status"])

    def mark_in_progress(self, application):
        if not self.has_capacity and self.accepted_application and self.accepted_application != application:
            raise ValidationError("Zlecenie ma już wybranego pomagającego.")
        self.accepted_application = application
        self.status = self.STATUS_IN_PROGRESS
        self.save(update_fields=["accepted_application", "status"])

    def complete(self):
        self.status = self.STATUS_COMPLETED
        self.save(update_fields=["status"])

    def cancel(self):
        self.status = self.STATUS_CANCELLED
        self.save(update_fields=["status"])

    @property
    def has_capacity(self):
        if self.helpers_needed <= 0:
            return False
        active_count = self.zgloszenia.filter(status="accepted").count()
        return active_count < self.helpers_needed
