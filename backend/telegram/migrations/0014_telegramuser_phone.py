# Generated by Django 4.2.10 on 2024-03-14 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0013_alter_telegramuser_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
