from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("jobs", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Zgloszenie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("wiadomosc", models.TextField()),
                ("proponowana_stawka", models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Oczekujące"),
                            ("accepted", "Zaakceptowane"),
                            ("declined", "Odrzucone"),
                            ("cancelled", "Anulowane"),
                        ],
                        default="pending",
                        max_length=12,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "wykonawca",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="zgloszenia",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "zlecenie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="zgloszenia", to="jobs.zlecenie"
                    ),
                ),
            ],
            options={
                "verbose_name": "Zgłoszenie",
                "verbose_name_plural": "Zgłoszenia",
            },
        ),
        migrations.AlterUniqueTogether(
            name="zgloszenie",
            unique_together={("zlecenie", "wykonawca")},
        ),
    ]
