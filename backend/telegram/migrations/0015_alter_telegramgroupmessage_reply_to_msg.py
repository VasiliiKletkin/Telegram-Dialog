# Generated by Django 4.2.10 on 2024-09-06 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0014_remove_telegramgroupmessage_reply_to_msg_id_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramgroupmessage',
            name='reply_to_msg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='telegram.telegramgroupmessage'),
        ),
    ]
