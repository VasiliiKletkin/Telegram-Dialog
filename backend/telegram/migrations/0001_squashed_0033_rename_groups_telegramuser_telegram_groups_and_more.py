# Generated by Django 4.2.10 on 2024-03-25 09:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    replaces = [('telegram', '0001_initial'), ('telegram', '0002_remove_telegramgroup_created_at_and_more'), ('telegram', '0003_remove_telegramgroup_group_id_and_more'), ('telegram', '0004_telegramuser_is_active_telegramuser_proxy_server'), ('telegram', '0005_remove_telegramuser_json_file_and_more'), ('telegram', '0006_telegramuserupload'), ('telegram', '0007_telegramgroup_name_alter_telegramgroup_id_and_more'), ('telegram', '0008_delete_telegramuserupload'), ('telegram', '0009_alter_telegramuser_is_active'), ('telegram', '0010_rename_session_telegramuser_client_session'), ('telegram', '0011_telegramgroupmessage'), ('telegram', '0012_telegramuser_error'), ('telegram', '0013_alter_telegramuser_error'), ('telegram', '0014_telegramuser_phone'), ('telegram', '0015_telegramuser_two_fa'), ('telegram', '0016_alter_telegramuser_phone_alter_telegramuser_two_fa'), ('telegram', '0017_alter_telegramuser_phone_alter_telegramuser_two_fa'), ('telegram', '0018_alter_telegramuser_app_and_more'), ('telegram', '0019_alter_telegramuser_proxy_server'), ('telegram', '0020_alter_telegramuser_app'), ('telegram', '0021_alter_telegramgroupmessage_reply_to_msg_id'), ('telegram', '0022_rename_message_telegramgroupmessage_text_and_more'), ('telegram', '0023_alter_telegramgroupmessage_user_id'), ('telegram', '0024_alter_telegramgroupmessage_unique_together_and_more'), ('telegram', '0025_telegramuser_sex'), ('telegram', '0026_alter_telegramuser_sex'), ('telegram', '0027_alter_telegramuser_sex'), ('telegram', '0028_alter_telegramuser_sex'), ('telegram', '0029_alter_telegramgroupmessage_options'), ('telegram', '0030_alter_telegramuser_is_active'), ('telegram', '0031_alter_telegramgroup_username'), ('telegram', '0032_alter_telegramgroupmessage_options_and_more'), ('telegram', '0033_rename_groups_telegramuser_telegram_groups_and_more')]

    initial = True

    dependencies = [
        ('proxies', '0007_alter_proxyserver_error'),
        ('proxies', '0001_initial'),
        ('django_telethon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(default=1, max_length=255)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramGroupMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.BigIntegerField()),
                ('user_id', models.BigIntegerField(blank=True, null=True)),
                ('reply_to_msg_id', models.BigIntegerField(blank=True, null=True)),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
                ('telegram_group', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='telegram.telegramgroup')),
            ],
            options={
                'unique_together': {('telegram_group', 'message_id')},
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('first_name', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('proxy_server', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='telegram_user', to='proxies.proxyserver')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_telethon.app')),
                ('app_json', models.JSONField(blank=True, null=True)),
                ('client_session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='django_telethon.clientsession')),
                ('error', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('two_fa', models.CharField(blank=True, max_length=30, null=True)),
                ('sex', models.PositiveIntegerField(blank=True, choices=[(0, 'Male'), (1, 'Female')], null=True)),
                ('telegram_groups', models.ManyToManyField(related_name='telegram_users', to='telegram.telegramgroup')),
            ],
        ),
    ]
