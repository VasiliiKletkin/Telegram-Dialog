# Generated by Django 4.2.10 on 2024-03-13 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxies', '0005_proxyserver_created_proxyserver_info_check_proxy_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proxyserver',
            name='info_check_proxy',
        ),
        migrations.AddField(
            model_name='proxyserver',
            name='error',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]