# Generated by Django 4.2.11 on 2024-05-10 18:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_alter_licensekey_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensekey',
            name='key',
            field=models.CharField(default=uuid.UUID('0e75c218-a624-40de-89c0-6c0eb2b0b104'), max_length=64),
        ),
    ]