# Generated by Django 4.2.10 on 2024-03-14 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0015_telegramuser_two_fa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='phone',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='two_fa',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]