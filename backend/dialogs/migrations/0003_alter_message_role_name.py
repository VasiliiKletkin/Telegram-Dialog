# Generated by Django 4.2.10 on 2024-04-04 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='role_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
