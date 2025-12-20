from django.conf import settings
from django.db import models
from django.utils import timezone

from jobs.models import Zlecenie


class Wiadomosc(models.Model):
    zlecenie = models.ForeignKey(Zlecenie, on_delete=models.CASCADE, related_name="wiadomosci")
    nadawca = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wyslane_wiadomosci")
    odbiorca = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otrzymane_wiadomosci")
    tresc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"

    def __str__(self):
        return f"{self.nadawca} -> {self.odbiorca}"

    def mark_read(self):
        if not self.read_at:
            self.read_at = timezone.now()
            self.save(update_fields=["read_at"])
