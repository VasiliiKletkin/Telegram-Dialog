# Generated by Django 4.2.10 on 2024-09-16 19:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0009_remove_dialog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialogmessage',
            name='delay',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
