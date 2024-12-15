"""
Models for timetable app.
"""

import datetime
from math import floor

from django.db import models
from django.urls import reverse

from curriculum.models import CurriculumLesson


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

