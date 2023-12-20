# Generated by Django 4.2.6 on 2023-12-20 11:40

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_groupsemester_semester_num_gte_0'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(validators=[polls.models.Student.validate_date]),
        ),
        migrations.AddConstraint(
            model_name='curriculum',
            constraint=models.CheckConstraint(check=models.Q(('duration__gte', 0)), name='duration_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='lessontime',
            constraint=models.CheckConstraint(check=models.Q(('end_time__gt', models.F('start_time'))), name='check_start_time'),
        ),
    ]