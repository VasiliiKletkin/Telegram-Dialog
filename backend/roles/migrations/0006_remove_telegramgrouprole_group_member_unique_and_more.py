# Generated by Django 4.2.10 on 2024-09-10 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0005_remove_telegramgrouprole_group_member_unique_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='telegramgrouprole',
            name='group_member_unique',
        ),
        migrations.RemoveConstraint(
            model_name='telegramgrouprole',
            name='group_actor_unique',
        ),
        migrations.RenameField(
            model_name='telegramgrouprole',
            old_name='group',
            new_name='source',
        ),
        migrations.AddConstraint(
            model_name='telegramgrouprole',
            constraint=models.UniqueConstraint(fields=('source', 'member'), name='group_member_unique'),
        ),
        migrations.AddConstraint(
            model_name='telegramgrouprole',
            constraint=models.UniqueConstraint(fields=('source', 'actor'), name='source_actor_unique'),
        ),
    ]
