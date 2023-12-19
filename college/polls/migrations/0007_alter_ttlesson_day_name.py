# Generated by Django 4.2.6 on 2023-12-19 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_curriculumlesson_lesson_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttlesson',
            name='day_name',
            field=models.CharField(choices=[('MON', 'Понедельник'), ('TUE', 'Вторник'), ('WED', 'Среда'), ('THU', 'Четверг'), ('FRI', 'Пятница'), ('SAT', 'Суббота'), ('SUN', 'Воскресенье')], max_length=3),
        ),
    ]
