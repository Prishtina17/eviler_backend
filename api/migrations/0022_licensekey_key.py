# Generated by Django 4.2.11 on 2024-05-10 18:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_licensekey_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='licensekey',
            name='key',
            field=models.CharField(default=uuid.UUID('6eb29cfa-31fb-4d55-8bf4-4371b3a5d41f'), max_length=64, unique=True),
        ),
    ]
