# Generated by Django 4.2.10 on 2024-09-23 16:16

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=64, null=True)),
                ('last_name', models.CharField(blank=True, max_length=64, null=True)),
                ('lang_code', models.CharField(blank=True, max_length=8, null=True)),
                ('phone', models.CharField(blank=True, max_length=32, null=True)),
                ('sex', models.PositiveIntegerField(blank=True, choices=[(1, 'Male'), (0, 'Female')], null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['username'], name='username_idx'), models.Index(fields=['first_name'], name='first_name_idx'), models.Index(fields=['last_name'], name='last_name_idx')],
            },
        ),
        migrations.CreateModel(
            name='BaseClientUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('telegram_users.telegramuser',),
        ),
        migrations.CreateModel(
            name='MemberUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('telegram_users.telegramuser',),
        ),
        migrations.CreateModel(
            name='ActorUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('telegram_users.baseclientuser',),
        ),
        migrations.CreateModel(
            name='ListenerUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('telegram_users.baseclientuser',),
        ),
    ]
