from django.contrib import admin

from .models import Wiadomosc


@admin.register(Wiadomosc)
class WiadomoscAdmin(admin.ModelAdmin):
    list_display = ["zlecenie", "nadawca", "odbiorca", "created_at", "read_at"]
    list_filter = ["created_at", "read_at"]
