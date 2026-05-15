# Generated manually for voice_preset field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("characters", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aicharacter",
            name="voice_preset",
            field=models.CharField(default="shaonv", max_length=32),
        ),
    ]
