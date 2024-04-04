# Generated by Django 4.2.11 on 2024-04-04 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_activesession_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evileruser',
            name='license_key',
        ),
        migrations.AddField(
            model_name='licensekey',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='licensekey',
            name='key',
            field=models.CharField(default=uuid.UUID('341c8ec6-8a2b-494d-a7d7-1cfc72909466'), max_length=64, unique=True),
        ),
    ]
