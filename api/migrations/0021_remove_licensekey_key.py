# Generated by Django 4.2.11 on 2024-05-10 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_licensekey_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='licensekey',
            name='key',
        ),
    ]