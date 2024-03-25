# Generated by Django 4.2.10 on 2024-03-25 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0034_alter_telegramgroup_name_and_more'),
        ('dialogs', '0001_squashed_0022_alter_scene_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='role_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='scene',
            name='telegram_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram.telegramgroup'),
        ),
    ]
