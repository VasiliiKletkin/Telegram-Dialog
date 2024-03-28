# Generated by Django 4.2.10 on 2024-03-27 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0037_alter_telegramgroup_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='sex',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Male'), (0, 'Female')], null=True),
        ),
    ]