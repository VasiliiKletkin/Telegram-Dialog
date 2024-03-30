# Generated by Django 4.2.10 on 2024-03-30 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0024_dialog_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='message',
            name='role_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
