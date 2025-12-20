from django.contrib import admin

from .models import Zgloszenie


@admin.register(Zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
    list_display = ["zlecenie", "wykonawca", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["zlecenie__tytul", "wykonawca__username"]
