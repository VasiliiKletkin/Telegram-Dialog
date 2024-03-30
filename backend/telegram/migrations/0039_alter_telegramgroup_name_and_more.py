# Generated by Django 4.2.10 on 2024-03-30 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0038_alter_telegramuser_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramgroup',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='telegramgroup',
            name='username',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='telegramgroupmessage',
            name='message_id',
            field=models.BigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='telegramgroupmessage',
            name='reply_to_msg_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='telegramgroupmessage',
            name='user_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(blank=True, db_index=True, default='', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='last_name',
            field=models.CharField(blank=True, db_index=True, default='', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='username',
            field=models.CharField(blank=True, db_index=True, max_length=32, null=True),
        ),
    ]
