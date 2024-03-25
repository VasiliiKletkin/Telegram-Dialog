# Generated by Django 4.2.10 on 2024-03-24 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_telethon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateStateClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_id', models.IntegerField()),
                ('client_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_telethon.clientsession')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_telethon.updatestate')),
            ],
            options={
                'unique_together': {('entity_id', 'client_session')},
            },
        ),
    ]
