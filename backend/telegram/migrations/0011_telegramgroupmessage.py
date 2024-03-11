# Generated by Django 4.2.10 on 2024-03-11 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0010_rename_session_telegramuser_client_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramGroupMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.BigIntegerField()),
                ('user_id', models.BigIntegerField()),
                ('reply_to_msg_id', models.BigIntegerField()),
                ('message', models.TextField()),
                ('date', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram.telegramgroup')),
            ],
        ),
    ]
