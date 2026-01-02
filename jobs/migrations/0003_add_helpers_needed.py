from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0002_add_accepted_application"),
    ]

    operations = [
        migrations.AddField(
            model_name="zlecenie",
            name="helpers_needed",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
