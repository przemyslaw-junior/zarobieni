from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0001_initial"),
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="zlecenie",
            name="accepted_application",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="applications.zgloszenie",
            ),
        ),
    ]
