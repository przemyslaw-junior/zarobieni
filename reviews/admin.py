from django.contrib import admin

from .models import Opinia


@admin.register(Opinia)
class OpiniaAdmin(admin.ModelAdmin):
    list_display = ["zlecenie", "reviewee", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["zlecenie__tytul", "reviewee__username"]
