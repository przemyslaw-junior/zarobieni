from django.conf import settings
from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfilWykonawcy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "stawka_h",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=6,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Stawka za godzinę",
                    ),
                ),
                (
                    "dostepnosc",
                    models.CharField(
                        choices=[("weekdays", "Dni robocze"), ("weekend", "Weekend"), ("flex", "Elastyczna")],
                        default="flex",
                        max_length=16,
                    ),
                ),
                ("kategorie", models.JSONField(blank=True, default=list)),
                ("bio", models.TextField(blank=True)),
                ("ok_dla_niepelnoletnich", models.BooleanField(default=False)),
                ("rating_avg", models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ("rating_count", models.PositiveIntegerField(default=0)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="worker_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Profil wykonawcy",
                "verbose_name_plural": "Profile wykonawców",
            },
        ),
    ]
