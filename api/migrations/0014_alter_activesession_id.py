# Generated by Django 4.2.11 on 2024-04-04 13:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_licensekey_evileruser_license_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activesession',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
