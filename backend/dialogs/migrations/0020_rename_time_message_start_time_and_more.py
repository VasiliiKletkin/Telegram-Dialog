# Generated by Django 4.2.10 on 2024-03-24 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0019_scene_start_date_alter_scene_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='time',
            new_name='start_time',
        ),
        migrations.AlterUniqueTogether(
            name='message',
            unique_together={('dialog', 'role_name', 'start_time')},
        ),
    ]