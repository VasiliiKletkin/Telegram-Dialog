# Generated by Django 4.2.10 on 2024-09-08 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxies', '0003_rename_error_proxyserver_errors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxyserver',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]