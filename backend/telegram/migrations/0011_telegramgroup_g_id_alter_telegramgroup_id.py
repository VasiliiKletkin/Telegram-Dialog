# Generated by Django 4.2.10 on 2024-09-04 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0010_alter_telegramgroup_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramgroup',
            name='g_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='telegramgroup',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
