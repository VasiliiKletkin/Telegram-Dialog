# Generated by Django 4.2.10 on 2024-09-09 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_groups', '0002_alter_telegramgroupdrain_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramgroupdrain',
            name='last_check',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='telegramgroupsource',
            name='last_check',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
