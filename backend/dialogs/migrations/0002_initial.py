# Generated by Django 4.2.10 on 2024-04-04 06:43

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('telegram', '0001_initial'),
        ('dialogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramgroupdialog',
            name='telegram_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram.telegramgroup'),
        ),
        migrations.AddField(
            model_name='scene',
            name='dialog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scenes', to='dialogs.dialog'),
        ),
        migrations.AddField(
            model_name='scene',
            name='telegram_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram.telegramgroup'),
        ),
        migrations.AddField(
            model_name='role',
            name='scene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='dialogs.scene'),
        ),
        migrations.AddField(
            model_name='role',
            name='telegram_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='telegram.telegramuser'),
        ),
        migrations.AddField(
            model_name='message',
            name='dialog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='dialogs.dialog'),
        ),
        migrations.AddField(
            model_name='message',
            name='reply_to_msg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dialogs.message'),
        ),
        migrations.AddField(
            model_name='dialog',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterUniqueTogether(
            name='telegramgroupdialog',
            unique_together={('telegram_group', 'dialog')},
        ),
        migrations.AlterUniqueTogether(
            name='scene',
            unique_together={('dialog', 'telegram_group')},
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('scene', 'telegram_user', 'name')},
        ),
    ]
