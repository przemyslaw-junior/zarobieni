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
            name="Wiadomosc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("tresc", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                (
                    "nadawca",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wyslane_wiadomosci",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "odbiorca",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="otrzymane_wiadomosci",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "zlecenie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wiadomosci",
                        to="jobs.zlecenie",
                    ),
                ),
            ],
            options={
                "verbose_name": "Wiadomość",
                "verbose_name_plural": "Wiadomości",
                "ordering": ["created_at"],
            },
        ),
    ]
