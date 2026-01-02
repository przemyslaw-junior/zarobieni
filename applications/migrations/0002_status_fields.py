from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("applications", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="zgloszenie",
            name="completed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="zgloszenie",
            name="decided_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="zgloszenie",
            name="decided_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="decided_applications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="zgloszenie",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Oczekujace"),
                    ("accepted", "Zaakceptowane"),
                    ("rejected", "Odrzucone"),
                    ("completed", "Zakonczone"),
                ],
                default="pending",
                max_length=12,
            ),
        ),
    ]
