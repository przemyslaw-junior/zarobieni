from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("jobs", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Opinia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("rating", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reviewee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="otrzymane_opinie", to=settings.AUTH_USER_MODEL)),
                ("reviewer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="wystawione_opinie", to=settings.AUTH_USER_MODEL)),
                ("zlecenie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="opinie", to="jobs.zlecenie")),
            ],
            options={
                "verbose_name": "Opinia",
                "verbose_name_plural": "Opinie",
            },
        ),
        migrations.AlterUniqueTogether(
            name="opinia",
            unique_together={("zlecenie", "reviewer")},
        ),
    ]
