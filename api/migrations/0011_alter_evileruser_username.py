# Generated by Django 5.0.3 on 2024-03-17 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_evileruser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evileruser',
            name='username',
            field=models.CharField(unique=True),
        ),
    ]
