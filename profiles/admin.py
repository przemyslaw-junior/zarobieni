from django.contrib import admin

from .models import ProfilWykonawcy


@admin.register(ProfilWykonawcy)
class ProfilWykonawcyAdmin(admin.ModelAdmin):
    list_display = ["user", "stawka_h", "dostepnosc", "ok_dla_niepelnoletnich", "rating_avg", "rating_count"]
    list_filter = ["dostepnosc", "ok_dla_niepelnoletnich"]
