# Generated by Django 4.2.6 on 2023-12-20 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_alter_ttlesson_day_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='groupsemester',
            constraint=models.CheckConstraint(check=models.Q(('semester_num__gte', 0)), name='semester_num_gte_0'),
        ),
    ]