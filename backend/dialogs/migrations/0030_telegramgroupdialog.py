# Generated by Django 4.2.10 on 2024-04-03 12:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0047_delete_telegramgroupdialog'),
        ('dialogs', '0029_remove_dialog_from_telegram_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramGroupDialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateTimeField()),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dialogs.dialog')),
                ('telegram_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram.telegramgroup')),
            ],
            options={
                'unique_together': {('telegram_group', 'dialog')},
            },
        ),
    ]
