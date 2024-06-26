# Generated by Django 5.0.3 on 2024-03-27 18:34

import computed_property.fields
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import timetable.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('timetable', '0001_initial'), ('timetable', '0002_tutors_students_constraints')]

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('classroom_id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'classroom',
            },
        ),
        migrations.CreateModel(
            name='Coefficient',
            fields=[
                ('coefficient_id', models.AutoField(primary_key=True, serialize=False)),
                ('coef_num', models.PositiveSmallIntegerField()),
                ('description', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'coefficient',
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('curriculum_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'curriculums',
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('discipline_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'disciplines',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16, unique=True)),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('hw_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=2048)),
                ('hw_type', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'homework',
            },
        ),
        migrations.CreateModel(
            name='LessonTime',
            fields=[
                ('lesson_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
            options={
                'db_table': 'lessons_time',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_birth', models.DateField(validators=[timetable.models.Student.validate_date])),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('attendance_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_present', models.BooleanField()),
            ],
            options={
                'db_table': 'students_attendance',
            },
        ),
        migrations.CreateModel(
            name='StudentProgress',
            fields=[
                ('progress_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'students_progress',
            },
        ),
        migrations.CreateModel(
            name='TTLesson',
            fields=[
                ('tt_lesson_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('day_name', models.CharField(choices=[('MON', 'Понедельник'), ('TUE', 'Вторник'), ('WED', 'Среда'), ('THU', 'Четверг'), ('FRI', 'Пятница'), ('SAT', 'Суббота'), ('SUN', 'Воскресенье')], max_length=3)),
                ('week_type', models.CharField(choices=[('EV', 'Четная неделя'), ('NE', 'Нечетная неделя'), ('CW', 'Зачетная неделя'), ('EX', 'Экзаменационная неделя')], max_length=2)),
            ],
            options={
                'db_table': 'tt_lesson',
            },
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('tutor_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_birth', models.DateField(validators=[timetable.models.Tutor.validate_date])),
            ],
            options={
                'db_table': 'tutors',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=128, verbose_name='first name')),
                ('last_name', models.CharField(max_length=128, verbose_name='last name')),
                ('second_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='second name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CurriculumLesson',
            fields=[
                ('curriculum_lesson_id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson_type', models.CharField(choices=[('PRA', 'Практика'), ('LEC', 'Лекция'), ('LAB', 'Лабораторная работа'), ('CRD', 'Зачет'), ('EXM', 'Экзамен')], max_length=3)),
                ('duration', models.PositiveSmallIntegerField()),
                ('curriculum_id', models.ForeignKey(db_column='curriculum_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.curriculum')),
            ],
            options={
                'db_table': 'curriculum_lessons',
            },
        ),
        migrations.AddField(
            model_name='curriculum',
            name='discipline_id',
            field=models.ForeignKey(db_column='discipline_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.discipline'),
        ),
        migrations.CreateModel(
            name='FinalGrade',
            fields=[
                ('final_grade_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_final', models.BooleanField()),
                ('scale_100', models.PositiveSmallIntegerField()),
                ('scale_5', computed_property.fields.ComputedIntegerField(compute_from='calc_scale_5', editable=False)),
                ('scale_word', computed_property.fields.ComputedTextField(compute_from='calc_scale_word', editable=False, max_length=128)),
                ('scale_letter', computed_property.fields.ComputedCharField(compute_from='calc_scale_letter', editable=False, max_length=1)),
                ('curriculum_id', models.ForeignKey(db_column='curriculum_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.curriculum')),
            ],
            options={
                'db_table': 'final_grades',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('grade_id', models.AutoField(primary_key=True, serialize=False)),
                ('scale_5', models.PositiveSmallIntegerField()),
                ('scale_word', models.CharField(max_length=32)),
                ('scale_100', models.PositiveSmallIntegerField()),
                ('scale_letter', models.CharField(max_length=1)),
                ('coef_num', models.PositiveSmallIntegerField()),
                ('coef_description', models.CharField(max_length=64)),
                ('coefficient_id', models.ForeignKey(db_column='coefficient_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.coefficient')),
            ],
            options={
                'db_table': 'grade',
            },
        ),
        migrations.CreateModel(
            name='GroupSemester',
            fields=[
                ('group_semester_id', models.AutoField(primary_key=True, serialize=False)),
                ('semester_num', models.PositiveSmallIntegerField()),
                ('group_id', models.ForeignKey(db_column='group_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.group')),
            ],
            options={
                'db_table': 'group_semesters',
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('group_member_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_semesters', models.ForeignKey(db_column='group_semester_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.groupsemester')),
            ],
            options={
                'db_table': 'group_members',
            },
        ),
        migrations.AddField(
            model_name='curriculum',
            name='group_semester_id',
            field=models.ForeignKey(db_column='group_semester_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.groupsemester'),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(blank=True, max_length=2048)),
                ('file', models.BinaryField()),
                ('hw_id', models.ForeignKey(db_column='hw_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.homework')),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.AddConstraint(
            model_name='lessontime',
            constraint=models.CheckConstraint(check=models.Q(('end_time__gt', models.F('start_time'))), name='check_start_time'),
        ),
        migrations.AddField(
            model_name='student',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='homework',
            name='student_id',
            field=models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.student'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='student_id',
            field=models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.student'),
        ),
        migrations.AddField(
            model_name='finalgrade',
            name='student_id',
            field=models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.student'),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='student_id',
            field=models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.student'),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='student_id',
            field=models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.student'),
        ),
        migrations.AddField(
            model_name='grade',
            name='progress_id',
            field=models.ForeignKey(db_column='progress_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.studentprogress'),
        ),
        migrations.AddField(
            model_name='ttlesson',
            name='classroom_id',
            field=models.ForeignKey(db_column='classroom_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.classroom'),
        ),
        migrations.AddField(
            model_name='ttlesson',
            name='curriculum_lesson_id',
            field=models.ForeignKey(db_column='curriculum_lesson_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.curriculumlesson'),
        ),
        migrations.AddField(
            model_name='ttlesson',
            name='lessons_time_id',
            field=models.ForeignKey(db_column='lessons_time_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.lessontime'),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='tt_lesson_id',
            field=models.ForeignKey(db_column='tt_lesson_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.ttlesson'),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='tt_lesson_id',
            field=models.ForeignKey(db_column='tt_lesson_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.ttlesson'),
        ),
        migrations.AddField(
            model_name='homework',
            name='day_due',
            field=models.ForeignKey(db_column='day_due', on_delete=django.db.models.deletion.PROTECT, related_name='day_due', to='timetable.ttlesson'),
        ),
        migrations.AddField(
            model_name='homework',
            name='day_given',
            field=models.ForeignKey(db_column='day_given', on_delete=django.db.models.deletion.PROTECT, related_name='day_given', to='timetable.ttlesson'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='curriculumlesson',
            name='tutor_id',
            field=models.ForeignKey(db_column='tutor_id', on_delete=django.db.models.deletion.PROTECT, to='timetable.tutor'),
        ),
        migrations.AddConstraint(
            model_name='groupsemester',
            constraint=models.CheckConstraint(check=models.Q(('semester_num__lte', 10)), name='timetable_groupsemester_semester_num_lte_10'),
        ),
        migrations.AddConstraint(
            model_name='finalgrade',
            constraint=models.CheckConstraint(check=models.Q(('scale_5__lte', 5)), name='timetable_finalgrade_mark_scale_5_lte_5'),
        ),
        migrations.AddConstraint(
            model_name='finalgrade',
            constraint=models.CheckConstraint(check=models.Q(('scale_100__lte', 100)), name='timetable_finalgrade_mark_scale_100_lte_100'),
        ),
        migrations.AddConstraint(
            model_name='finalgrade',
            constraint=models.CheckConstraint(check=models.Q(('scale_word__in', ['отлично', 'хорошо', 'удовлетворительно', 'неудовлетворительно'])), name='timetable_finalgrade_mark_scale_word_correct'),
        ),
        migrations.AddConstraint(
            model_name='finalgrade',
            constraint=models.CheckConstraint(check=models.Q(('scale_letter__in', ['A', 'B', 'C', 'D', 'E', 'F'])), name='timetable_finalgrade_mark_scale_letter_correct'),
        ),
        migrations.AddConstraint(
            model_name='curriculumlesson',
            constraint=models.CheckConstraint(check=models.Q(('lesson_type__in', ['PRA', 'LEC', 'LAB', 'CRD', 'EXM'])), name='timetable_curriculumlesson_correct_lesson_type'),
        ),
        migrations.AddConstraint(
            model_name='curriculumlesson',
            constraint=models.CheckConstraint(check=models.Q(('duration__gte', 0)), name='timetable_curriculumlesson_duration_gte_0'),
        ),
        migrations.RunSQL(
            sql="ALTER TABLE students ADD CONSTRAINT timetable_students_age_correct CHECK (date_part('year', age(date_of_birth))::int >= 14 AND date_part('year', age(date_of_birth))::int <= 120);",
            reverse_sql='ALTER TABLE students DROP CONSTRAINT IF EXISTS timetable_students_age_correct;',
        ),
        migrations.RunSQL(
            sql="ALTER TABLE tutors ADD CONSTRAINT timetable_tutors_age_correct CHECK (date_part('year', age(date_of_birth))::int >= 18 AND date_part('year', age(date_of_birth))::int <= 120);",
            reverse_sql='ALTER TABLE tutors DROP CONSTRAINT IF EXISTS timetable_tutors_age_correct;',
        ),
    ]
