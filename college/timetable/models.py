"""
Models for account app.
"""

from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from computed_property import ComputedTextField, ComputedIntegerField, ComputedCharField


class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=128)
    last_name = models.CharField(_("last name"), max_length=128)
    second_name = models.CharField(_("second name"), max_length=128, null=True, blank=True)


class Student(models.Model):
    def validate_date(self: models.DateField()):
        today = date.today()
        age = today.year - self.year - ((today.month, today.day) < (self.month, self.day))
        if age < 14:
            raise ValidationError(
                _("%(value)s is less than 14"),
                params={"value": self},
            )

    student_id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField(validators=[validate_date])
    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, db_column='user_id')

    class Meta:
        db_table = 'students'


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, unique=True)

    class Meta:
        db_table = 'groups'


class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'disciplines'


class Tutor(models.Model):
    def validate_date(self: models.DateField()):
        today = date.today()
        age = today.year - self.year - ((today.month, today.day) < (self.month, self.day))
        if age < 18:
            raise ValidationError(
                _("%(value)s is less than 18"),
                params={"value": self},
            )

    tutor_id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField(validators=[validate_date])

    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, db_column='user_id')

    class Meta:
        db_table = 'tutors'


class GroupSemester(models.Model):
    group_semester_id = models.AutoField(primary_key=True)
    semester_num = models.PositiveSmallIntegerField()
    group_id = models.ForeignKey(Group, on_delete=models.PROTECT, db_column='group_id')

    class Meta:
        db_table = 'group_semesters'
        constraints = [
            models.CheckConstraint(
                check=models.Q(semester_num__lte=10),
                name="%(app_label)s_%(class)s_semester_num_lte_10"
            )
        ]


class GroupMember(models.Model):
    group_member_id = models.AutoField(primary_key=True)
    group_semesters = models.ForeignKey(GroupSemester, on_delete=models.PROTECT, db_column='group_semester_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'group_members'


class Curriculum(models.Model):
    curriculum_id = models.AutoField(primary_key=True)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.PROTECT, db_column='discipline_id')
    group_semester_id = models.ForeignKey(GroupSemester, on_delete=models.PROTECT, db_column='group_semester_id')

    class Meta:
        db_table = 'curriculums'


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


class TypesOfLesson(models.TextChoices):
    PRACTICE = "PRA", _("Практика")
    LECTURE = "LEC", _("Лекция")
    LABORATORY = "LAB", _("Лабораторная работа")
    CREDIT = "CRD", _("Зачет")
    EXAM = "EXM", _("Экзамен")


class CurriculumLesson(models.Model):
    curriculum_lesson_id = models.AutoField(primary_key=True)
    lesson_type = models.CharField(max_length=3,
                                   choices=TypesOfLesson.choices
                                   )
    duration = models.PositiveSmallIntegerField()
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.PROTECT, db_column='curriculum_id')
    tutor_id = models.ForeignKey(Tutor, on_delete=models.PROTECT, db_column='tutor_id')

    class Meta:
        db_table = 'curriculum_lessons'
        constraints = [
            models.CheckConstraint(
                check=models.Q(lesson_type__in=TypesOfLesson.values),
                name="%(app_label)s_%(class)s_correct_lesson_type",
            ),
            models.CheckConstraint(
                check=models.Q(duration__gte=0),
                name='%(app_label)s_%(class)s_duration_gte_0'
            )
        ]


class LessonTime(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'lessons_time'
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name='check_start_time',
            ),
        ]


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=8)

    class Meta:
        db_table = 'classroom'


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
    lessons_time_id = models.ForeignKey(LessonTime, on_delete=models.PROTECT, db_column='lessons_time_id')
    classroom_id = models.ForeignKey(Classroom, on_delete=models.PROTECT, db_column='classroom_id')
    curriculum_lesson_id = models.ForeignKey(CurriculumLesson, on_delete=models.PROTECT,
                                             db_column='curriculum_lesson_id')

    class Meta:
        db_table = 'tt_lesson'


class Homework(models.Model):
    INDIVIDUAL = "IND"
    GROUP = "GRP"
    TYPE_OF_TYPE_CHOICES = [
        (INDIVIDUAL, "индивидуальное"),
        (GROUP, "групповое")
    ]
    hw_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2048)
    day_given = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_given', db_column='day_given')
    day_due = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_due', db_column='day_due')
    hw_type = models.CharField(max_length=2, choices=TYPE_OF_TYPE_CHOICES)
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'homework'


class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=2048, blank=True)
    file = models.BinaryField()
    hw_id = models.ForeignKey(Homework, on_delete=models.PROTECT, db_column='hw_id')

    class Meta:
        db_table = 'files'


class StudentAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    is_present = models.BooleanField()
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT, db_column='tt_lesson_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'students_attendance'


class StudentProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT, db_column='tt_lesson_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'students_progress'


class Coefficient(models.Model):
    TYPE_OF_COEFFICIENT_CHOICES = [ 1, 2, 3, 4, 5 ]
    coefficient_id = models.AutoField(primary_key=True)
    coef_num = models.PositiveSmallIntegerField(сhoices=TYPE_OF_COEFFICIENT_CHOICES)
    description = models.CharField(max_length=64)

    class Meta:
        db_table = 'coefficients'


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    scale_100 = models.PositiveSmallIntegerField()
    scale_5 = ComputedIntegerField(compute_from='calc_scale_5')
    scale_word = ComputedTextField(max_length=128, compute_from='calc_scale_word')
    scale_letter = ComputedCharField(max_length=1, compute_from='calc_scale_letter')
    coef_num = models.PositiveSmallIntegerField()
    coef_description = models.CharField(max_length=64)
    coefficient_id = models.ForeignKey(Coefficient, on_delete=models.PROTECT, db_column='coefficient_id')
    progress_id = models.ForeignKey(StudentProgress, on_delete=models.PROTECT, db_column='progress_id')

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
