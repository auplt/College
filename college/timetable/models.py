"""
Models for timetable app.
"""

import datetime
from math import floor
from computed_property import ComputedTextField, ComputedIntegerField, ComputedCharField

from django.db import models
from django.urls import reverse

from user.models import Student, Tutor
from curriculum.models import Curriculum, CurriculumLesson


class LessonTime(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.name}: {datetime.time.strftime(self.start_time, "%H:%M")} - {datetime.time.strftime(self.end_time, "%H:%M")}'

    class Meta:
        db_table = 'lessons_times'
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name='check_start_time',
            ),
            models.UniqueConstraint(fields=['start_time', 'end_time'],
                                    name='lesson_time_start_time_end_time_unique')
        ]

    def get_absolute_url(self):
        return reverse('timetable:lesson_time_details',
                       args=[self.lesson_id])

    def get_edit_url(self):
        return reverse('timetable:lesson_time_edit',
                       args=[self.lesson_id])

    def get_delete_url(self):
        return reverse('timetable:lesson_time_delete',
                       args=[self.lesson_id])


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=8, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.number}'

    class Meta:
        db_table = 'classrooms'

    def get_absolute_url(self):
        return reverse('timetable:classroom_details',
                       args=[self.classroom_id])

    def get_edit_url(self):
        return reverse('timetable:classroom_edit',
                       args=[self.classroom_id])

    def get_delete_url(self):
        return reverse('timetable:classroom_delete',
                       args=[self.classroom_id])


class TTLesson(models.Model):
    EVEN_WEEK = "EV"
    NOT_EVEN_WEEK = "NE"
    CREDIT_WEEK = "CW"
    EXAM_WEEK = "EX"
    TYPE_OF_WEEK_CHOICES = [
        (EVEN_WEEK, "Четная неделя"),
        (NOT_EVEN_WEEK, "Нечетная неделя"),
        (CREDIT_WEEK, "Зачетная неделя"),
        (EXAM_WEEK, "Экзаменационная неделя")
    ]

    MONDAY = "MON"
    TUESDAY = "TUE"
    WEDNESDAY = "WED"
    THURSDAY = "THU"
    FRIDAY = "FRI"
    SATURDAY = "SAT"
    SUNDAY = "SUN"
    DAY_OF_WEEK_CHOICES = [
        (MONDAY, "Понедельник"),
        (TUESDAY, "Вторник"),
        (WEDNESDAY, "Среда"),
        (THURSDAY, "Четверг"),
        (FRIDAY, "Пятница"),
        (SATURDAY, "Суббота"),
        (SUNDAY, "Воскресенье")
    ]

    tt_lesson_id = models.AutoField(primary_key=True)
    date = models.DateField()
    day_name = models.CharField(max_length=3,
                                choices=DAY_OF_WEEK_CHOICES
                                )
    week_type = models.CharField(max_length=2,
                                 choices=TYPE_OF_WEEK_CHOICES
                                 )
    lesson_time_id = models.ForeignKey(LessonTime, on_delete=models.PROTECT, db_column='lesson_time_id')
    classroom_id = models.ForeignKey(Classroom, on_delete=models.PROTECT, db_column='classroom_id')
    curriculum_lesson_id = models.ForeignKey(CurriculumLesson, on_delete=models.PROTECT,
                                             db_column='curriculum_lesson_id')

    def set_day_name(self, lesson_date: datetime.date) -> None:
        self.day_name = lesson_date.strftime("%a").upper()

    def set_week_type(self, lesson_date: datetime.date) -> None:
        if lesson_date.month in [1, 7, 8]:
            self.week_type = 'EX'
        elif lesson_date.month in [9, 10, 11, 12]:
            start_date = datetime.date(lesson_date.year, 9, 1)
            week_num = floor((lesson_date - start_date).days / 7.0) + 1
            if start_date.weekday() == 6:
                week_num -= 1
                if lesson_date == start_date:
                    self.week_type = 'EX'
                    return
                start_date += datetime.timedelta(days=1)
            if lesson_date >= start_date + datetime.timedelta(days=16 * 7):
                self.week_type = 'CW'
            elif week_num % 2 == 0:
                self.week_type = 'EV'
            else:
                self.week_type = 'NE'
        elif lesson_date.month in [2, 3, 4, 5, 6]:
            start_date = datetime.date(lesson_date.year, 2, 1) + datetime.timedelta(days=7)
            if start_date.weekday() == 6 or start_date.weekday() == 5:
                start_date += datetime.timedelta(days=7 - start_date.weekday())
            week_num = floor((lesson_date - start_date).days / 7.0) + 1
            if lesson_date < start_date:
                self.week_type = 'EX'
                return
            if start_date + datetime.timedelta(days=15 * 7) <= lesson_date < start_date + datetime.timedelta(
                    days=16 * 7):
                self.week_type = 'CW'
            elif lesson_date.month == 6:
                self.week_type = 'EX'
            elif week_num % 2 == 0:
                self.week_type = 'EV'
            else:
                self.week_type = 'NE'

    @staticmethod
    def get_week_type(lesson_date: datetime.date) -> str:
        if lesson_date.month in [1, 7, 8]:
            return 'EX'
        elif lesson_date.month in [9, 10, 11, 12]:
            start_date = datetime.date(lesson_date.year, 9, 1)
            week_num = floor((lesson_date - start_date).days / 7.0) + 1
            if start_date.weekday() == 6:
                week_num -= 1
                if lesson_date == start_date:
                    return 'EX'
                start_date += datetime.timedelta(days=1)
            if lesson_date >= start_date + datetime.timedelta(days=16 * 7):
                return 'CW'
            elif week_num % 2 == 0:
                return 'EV'
            else:
                return 'NE'
        elif lesson_date.month in [2, 3, 4, 5, 6]:
            start_date = datetime.date(lesson_date.year, 2, 1) + datetime.timedelta(days=7)
            if start_date.weekday() == 6 or start_date.weekday() == 5:
                start_date += datetime.timedelta(days=7 - start_date.weekday())
            week_num = floor((lesson_date - start_date).days / 7.0) + 1
            if lesson_date < start_date:
                return 'EX'
            if start_date + datetime.timedelta(days=15 * 7) <= lesson_date < start_date + datetime.timedelta(
                    days=16 * 7):
                return 'CW'
            elif lesson_date.month == 6:
                return 'EX'
            elif week_num % 2 == 0:
                return 'EV'
            else:
                return 'NE'

    class Meta:
        db_table = 'tt_lessons'
        constraints = [
            models.UniqueConstraint(fields=['date', 'lesson_time_id', 'curriculum_lesson_id'],
                                    name='tt_lesson_date_time_curriculum_lesson_unique')
        ]


class GradesScaleWord:
    EXCELLENT = "отлично"
    GOOD = "хорошо"
    SATISFYING = "удовлетворительно"
    UNSATISFYING = "неудовлетворительно"


class FinalGrade(models.Model):
    final_grade_id = models.AutoField(primary_key=True)
    is_final = models.BooleanField()
    scale_100 = models.PositiveSmallIntegerField()
    scale_5 = ComputedIntegerField(compute_from='calc_scale_5')
    scale_word = ComputedTextField(max_length=128, compute_from='calc_scale_word')
    scale_letter = ComputedCharField(max_length=1, compute_from='calc_scale_letter')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.PROTECT, db_column='curriculum_id')

    @property
    def calc_scale_5(self):
        match self.scale_100:
            case grade if 100 >= grade >= 90:
                return 5
            case grade if 89 >= grade >= 70:
                return 4
            case grade if 69 >= grade >= 60:
                return 3
            case _:
                return 2

    @property
    def calc_scale_word(self):
        match self.scale_100:
            case grade if 100 >= grade >= 90:
                return GradesScaleWord.EXCELLENT
            case grade if 89 >= grade >= 70:
                return GradesScaleWord.GOOD
            case grade if 69 >= grade >= 60:
                return GradesScaleWord.SATISFYING
            case _:
                return GradesScaleWord.UNSATISFYING

    @property
    def calc_scale_letter(self):
        match self.scale_100:
            case grade if 100 >= grade >= 90:
                return "A"
            case grade if 89 >= grade >= 85:
                return "B"
            case grade if 84 >= grade >= 75:
                return "C"
            case grade if 74 >= grade >= 65:
                return "D"
            case grade if 64 >= grade >= 60:
                return "E"
            case _:
                return "F"

    class Meta:
        db_table = 'final_grades'
        constraints = [
            models.CheckConstraint(
                check=models.Q(scale_5__lte=5),
                name='%(app_label)s_%(class)s_mark_scale_5_lte_5'
            ),
            models.CheckConstraint(
                check=models.Q(scale_100__lte=100),
                name='%(app_label)s_%(class)s_mark_scale_100_lte_100'
            ),
            models.CheckConstraint(
                check=models.Q(
                    scale_word__in=[GradesScaleWord.EXCELLENT, GradesScaleWord.GOOD, GradesScaleWord.SATISFYING,
                                    GradesScaleWord.UNSATISFYING]),
                name='%(app_label)s_%(class)s_mark_scale_word_correct'
            ),
            models.CheckConstraint(
                check=models.Q(
                    scale_letter__in=["A", "B", "C", "D", "E", "F"]),
                name='%(app_label)s_%(class)s_mark_scale_letter_correct'
            )
        ]


class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=2048, blank=True)
    file = models.BinaryField()

    class Meta:
        db_table = 'files'


class Homework(models.Model):
    hw_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2048)
    day_given = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_given', db_column='day_given')
    day_due = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_due', db_column='day_due')
    hw_type = models.PositiveSmallIntegerField()
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    # file_id = models.ForeignKey(File, on_delete=models.PROTECT, db_column='file_id')

    class Meta:
        db_table = 'homeworks'


class StudentAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    is_present = models.BooleanField()
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT, db_column='tt_lesson_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'students_attendances'


class Coefficient(models.Model):
    coefficient_id = models.AutoField(primary_key=True)
    coef_num = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=64)

    class Meta:
        db_table = 'coefficients'


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    scale_5 = models.PositiveSmallIntegerField()
    scale_word = models.CharField(max_length=32)
    scale_100 = models.PositiveSmallIntegerField()
    scale_letter = models.CharField(max_length=1)
    coefficient_id = models.ForeignKey(Coefficient, on_delete=models.PROTECT, db_column='coefficient_id')

    @property
    def calc_scale_5(self):
        match self.scale_100:
            case grade if 100 >= grade >= 90:
                return 5
            case grade if 89 >= grade >= 70:
                return 4
            case grade if 69 >= grade >= 60:
                return 3
            case _:
                return 2

    @property
    def calc_scale_word(self):
        match self.scale_100:
            case grade if 100 >= grade >= 90:
                return GradesScaleWord.EXCELLENT
            case grade if 89 >= grade >= 70:
                return GradesScaleWord.GOOD
            case grade if 69 >= grade >= 60:
                return GradesScaleWord.SATISFYING
            case _:
                return GradesScaleWord.UNSATISFYING

    @property
    def calc_scale_letter(self):
        match self.scale_100:
            case grade if 100 >= grade >= 90:
                return "A"
            case grade if 89 >= grade >= 85:
                return "B"
            case grade if 84 >= grade >= 75:
                return "C"
            case grade if 74 >= grade >= 65:
                return "D"
            case grade if 64 >= grade >= 60:
                return "E"
            case _:
                return "F"

    class Meta:
        db_table = 'grades'
        constraints = [
            models.CheckConstraint(
                check=models.Q(scale_5__lte=5),
                name='%(app_label)s_%(class)s_mark_scale_5_lte_5'
            ),
            models.CheckConstraint(
                check=models.Q(scale_100__lte=100),
                name='%(app_label)s_%(class)s_mark_scale_100_lte_100'
            ),
            models.CheckConstraint(
                check=models.Q(
                    scale_word__in=[GradesScaleWord.EXCELLENT, GradesScaleWord.GOOD, GradesScaleWord.SATISFYING,
                                    GradesScaleWord.UNSATISFYING]),
                name='%(app_label)s_%(class)s_mark_scale_word_correct'
            ),
            models.CheckConstraint(
                check=models.Q(
                    scale_letter__in=["A", "B", "C", "D", "E", "F"]),
                name='%(app_label)s_%(class)s_mark_scale_letter_correct'
            )
        ]


class StudentProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT, db_column='tt_lesson_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')
    grade_id = models.ForeignKey(Grade, on_delete=models.PROTECT, db_column='grade_id')

    class Meta:
        db_table = 'students_progresses'
