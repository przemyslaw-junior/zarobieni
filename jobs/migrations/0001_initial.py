from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Zlecenie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("tytul", models.CharField(max_length=120)),
                ("opis", models.TextField()),
                ("kategoria", models.CharField(max_length=64)),
                ("miasto", models.CharField(max_length=64)),
                ("dzielnica", models.CharField(blank=True, max_length=64)),
                ("data_start", models.DateField()),
                ("czas_trwania_h", models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2)])),
                (
                    "stawka_h",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("ok_dla_niepelnoletnich", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("published", "Opublikowane"),
                            ("in_progress", "W trakcie"),
                            ("completed", "Zakończone"),
                            ("cancelled", "Anulowane"),
                        ],
                        default="published",
                        max_length=16,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="zlecenia",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Zlecenie",
                "verbose_name_plural": "Zlecenia",
                "ordering": ["-created_at"],
            },
        ),
    ]
