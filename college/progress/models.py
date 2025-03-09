"""
Models for progress app.
"""

from math import floor
from computed_property import ComputedTextField, ComputedIntegerField, ComputedCharField

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from user.models import Student
from curriculum.models import Curriculum
from timetable.models import TTLesson


class StudentAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    is_present = models.BooleanField(default=True)
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT, db_column='tt_lesson_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'students_attendances'


class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=2048, blank=True, null=True)
    file = models.BinaryField()

    class Meta:
        db_table = 'files'


class TypesOfHomework(models.TextChoices):
    INDIVIDUAL = "IND", _("Индивидуальное")
    GROUP = "GRP", _("Групповое")


class Homework(models.Model):
    hw_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2048)
    day_given = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_given', db_column='day_given')
    day_due = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_due', db_column='day_due')
    hw_type = models.CharField(max_length=3,
                                choices=TypesOfHomework.choices
                                )
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id', blank=True, null=True)
    file_id = models.ForeignKey(File, on_delete=models.PROTECT, db_column='file_id', blank=True, null=True)

    class Meta:
        db_table = 'homeworks'


class GradesScaleWord:
    EXCELLENT = "отлично"
    GOOD = "хорошо"
    SATISFYING = "удовлетворительно"
    UNSATISFYING = "неудовлетворительно"


class TypesOfFinalGrade(models.TextChoices):
    EXAM = "EXM", _("экзамен")
    CREDIT = "CRD", _("зачёт")
    SEMESTR1 = "SEM1", _("1 полусеместр")
    SEMESTR2 = "SEM2", _("2 полусеместр")


class FinalGrade(models.Model):
    final_grade_id = models.AutoField(primary_key=True)
    grade_type = models.CharField(max_length=4,
                                   choices=TypesOfFinalGrade.choices
                                   )
    scale_100 = models.PositiveSmallIntegerField()
    scale_5 = ComputedIntegerField(compute_from='calc_scale_5')
    scale_word = ComputedTextField(max_length=32, compute_from='calc_scale_word')
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


class Coefficient(models.Model):
    coefficient_id = models.AutoField(primary_key=True)
    coef_num = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=64)

    class Meta:
        db_table = 'coefficients'


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    scale_100 = models.PositiveSmallIntegerField()
    scale_5 = ComputedIntegerField(compute_from='calc_scale_5')
    scale_word = ComputedTextField(max_length=32, compute_from='calc_scale_word')
    scale_letter = ComputedCharField(max_length=1, compute_from='calc_scale_letter')
    coefficient_id = models.ForeignKey(Coefficient, on_delete=models.PROTECT, db_column='coefficient_id', default=1)

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
