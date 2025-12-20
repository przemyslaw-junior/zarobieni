from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    ROLE_CLIENT = "client"
    ROLE_WORKER = "worker"
    ROLE_CHOICES = [
        (ROLE_CLIENT, "Zleceniodawca"),
        (ROLE_WORKER, "Wykonawca"),
    ]

    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    city = models.CharField(max_length=64, blank=True)
    district = models.CharField(max_length=64, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=32, blank=True)

    def clean(self):
        if self.birth_date and self.age < 16:
            raise ValidationError("Użytkownik musi mieć co najmniej 16 lat.")

    @property
    def age(self):
        if not self.birth_date:
            return 0
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    @property
    def is_client(self):
        return self.role == self.ROLE_CLIENT

    @property
    def is_worker(self):
        return self.role == self.ROLE_WORKER

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"
