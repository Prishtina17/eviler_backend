# Generated by Django 4.2.7 on 2023-12-04 11:29

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_evileruser_email'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='evileruser',
            managers=[
                ('objects', api.models.EvilerUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='evileruser',
            name='discord_id',
            field=models.BigIntegerField(default=-1),
        ),
    ]
