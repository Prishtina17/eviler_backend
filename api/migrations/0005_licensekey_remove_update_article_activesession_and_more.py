# Generated by Django 4.2.7 on 2023-12-13 07:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_discord_evileruser_discord_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='None', max_length=64)),
                ('sessionsLimit', models.PositiveIntegerField(default=5)),
                ('renewalExpiration', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='update',
            name='article',
        ),
        migrations.CreateModel(
            name='ActiveSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fingerprint', models.CharField(default='None', max_length=64)),
                ('expiration', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.licensekey')),
            ],
        ),
        migrations.AddField(
            model_name='update',
            name='Article',
            field=models.CharField(default='Article', max_length=500),
        ),
    ]
