# Generated by Django 4.2.11 on 2024-05-10 18:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_licensekey_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensekey',
            name='key',
            field=models.CharField(default=uuid.UUID('9df4f504-3d54-46b7-8f20-d4e48c64275c'), max_length=64),
        ),
    ]
