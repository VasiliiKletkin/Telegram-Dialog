# Generated by Django 4.2.10 on 2024-03-11 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0011_telegramgroupmessage'),
        ('dialogs', '0005_scene_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='telegram_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='telegram.telegramuser'),
        ),
    ]