from django.contrib import admin

from .models import Zlecenie


@admin.register(Zlecenie)
class ZlecenieAdmin(admin.ModelAdmin):
    list_display = ["tytul", "owner", "miasto", "stawka_h", "status", "ok_dla_niepelnoletnich"]
    list_filter = ["status", "miasto", "ok_dla_niepelnoletnich"]
    search_fields = ["tytul", "opis", "owner__username"]
