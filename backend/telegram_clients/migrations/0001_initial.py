# Generated by Django 4.2.10 on 2024-10-01 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proxies', '0001_initial'),
        ('djelethon', '0001_initial'),
        ('telegram_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('last_check', models.DateTimeField(blank=True, null=True)),
                ('errors', models.TextField(blank=True, null=True)),
                ('is_listener', models.BooleanField(default=False)),
                ('two_fa', models.CharField(max_length=30)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djelethon.app')),
                ('proxy', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to='proxies.proxyserver')),
                ('session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='djelethon.clientsession')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='telegram_users.telegramuser')),
            ],
        ),
    ]
