# Generated by Django 4.2.10 on 2024-03-13 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0012_telegramuser_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='error',
            field=models.TextField(blank=True, null=True),
        ),
    ]
