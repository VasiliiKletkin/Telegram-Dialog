# Generated by Django 4.2.10 on 2024-04-04 06:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_telethon', '0001_initial'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('proxies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('similar_groups', models.ManyToManyField(blank=True, null=True, to='telegram.telegramgroup')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True)),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('first_name', models.CharField(blank=True, db_index=True, default='', max_length=64, null=True)),
                ('last_name', models.CharField(blank=True, db_index=True, default='', max_length=64, null=True)),
                ('sex', models.PositiveIntegerField(blank=True, choices=[(1, 'Male'), (0, 'Female')], null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('two_fa', models.CharField(blank=True, max_length=30, null=True)),
                ('app_json', models.JSONField(blank=True, null=True)),
                ('error', models.TextField(blank=True, null=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_telethon.app')),
                ('client_session', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='django_telethon.clientsession')),
                ('proxy_server', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='telegram_user', to='proxies.proxyserver')),
                ('telegram_groups', models.ManyToManyField(blank=True, null=True, related_name='telegram_users', to='telegram.telegramgroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TelegramGroupMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.BigIntegerField(db_index=True)),
                ('text', models.TextField(db_index=True)),
                ('date', models.DateTimeField()),
                ('user_id', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('reply_to_msg_id', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('telegram_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='telegram.telegramgroup')),
            ],
            options={
                'unique_together': {('telegram_group', 'message_id')},
            },
        ),
    ]
