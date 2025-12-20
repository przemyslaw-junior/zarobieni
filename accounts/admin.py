from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Dodatkowe dane",
            {"fields": ("role", "city", "district", "birth_date", "phone_number")},
        ),
    )
    list_display = ["username", "email", "role", "city", "district"]
    list_filter = ["role", "city"]
