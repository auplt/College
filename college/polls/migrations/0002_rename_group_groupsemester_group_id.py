# Generated by Django 4.2.6 on 2023-12-19 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupsemester',
            old_name='group',
            new_name='group_id',
        ),
    ]
