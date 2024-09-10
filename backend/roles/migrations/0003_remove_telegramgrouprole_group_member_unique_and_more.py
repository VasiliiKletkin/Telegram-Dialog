# Generated by Django 4.2.10 on 2024-09-10 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0002_rename_group_telegramgrouprole_source'),
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
        migrations.AddConstraint(
            model_name='telegramgrouprole',
            constraint=models.UniqueConstraint(fields=('source', 'member'), name='group_member_unique'),
        ),
        migrations.AddConstraint(
            model_name='telegramgrouprole',
            constraint=models.UniqueConstraint(fields=('source', 'actor'), name='source_actor_unique'),
        ),
    ]
