# Generated by Django 4.2.7 on 2023-12-01 10:43

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_activemodule_module'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activemodule',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.fields.NOT_PROVIDED, to='api.module'),
        ),
    ]
