# Generated by Django 4.2.10 on 2024-03-22 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0025_telegramuser_sex'),
        ('dialogs', '0014_dialog_tags_alter_role_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='role',
            new_name='name',
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('scene', 'telegram_user', 'name')},
        ),
    ]