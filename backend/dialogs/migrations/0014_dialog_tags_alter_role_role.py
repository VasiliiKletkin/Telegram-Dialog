# Generated by Django 4.2.10 on 2024-03-22 07:46

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('dialogs', '0013_message_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialog',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.PositiveBigIntegerField(),
        ),
    ]