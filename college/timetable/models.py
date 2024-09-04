"""
Models for account app.
"""

from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from computed_property import ComputedTextField, ComputedIntegerField, ComputedCharField
from django.urls import reverse


class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=128)
    last_name = models.CharField(_("last name"), max_length=128)
    second_name = models.CharField(_("second name"), max_length=128, null=True, blank=True)

    # def __str__(self):
    #     return super().__str__
    # #     return f'{self.last_name} {self.first_name} {self.second_name}'

    def get_absolute_url(self):
        return reverse('account:user_details',
                       args=[self.id])

    def get_edit_url(self):
        return reverse('account:user_edit',
                       args=[self.id])

    def get_delete_url(self):
        return reverse('account:user_delete',
                       args=[self.id])


class Student(models.Model):
    def validate_date(self: models.DateField()):
        today = date.today()
        age = today.year - self.year - ((today.month, today.day) < (self.month, self.day))
        if age < 14:
            raise ValidationError(
                _("%(value)s is less than 14"),
                params={"value": self},
            )

    def set_user_id(self, user_id):
        self.user_id = user_id

    student_id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField(validators=[validate_date])
    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, db_column='user_id')

    def __str__(self):
        return f'{self.user_id.last_name} {self.user_id.first_name} {self.user_id.second_name}'

    class Meta:
        db_table = 'students'


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'groups'

    def get_absolute_url(self):
        return reverse('account:group_details',
                       args=[self.group_id])

    def get_edit_url(self):
        return reverse('account:group_edit',
                       args=[self.group_id])

    def get_delete_url(self):
        return reverse('account:group_delete',
                       args=[self.group_id])


class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'disciplines'

    def get_absolute_url(self):
        return reverse('account:discipline_details',
                       args=[self.discipline_id])

    def get_edit_url(self):
        return reverse('account:discipline_edit',
                       args=[self.discipline_id])

    def get_delete_url(self):
        return reverse('account:discipline_delete',
                       args=[self.discipline_id])


class Tutor(models.Model):
    def validate_date(self: models.DateField()):
        today = date.today()
        age = today.year - self.year - ((today.month, today.day) < (self.month, self.day))
        if age < 18:
            raise ValidationError(
                _("%(value)s is less than 18"),
                params={"value": self},
            )

    def set_user_id(self, user_id):
        self.user_id = user_id

    tutor_id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField(validators=[validate_date])

    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, db_column='user_id')

    def __str__(self):
        return f'{self.user_id.last_name} {self.user_id.first_name} {self.user_id.second_name}'

    class Meta:
        db_table = 'tutors'


class GroupSemester(models.Model):
    group_semester_id = models.AutoField(primary_key=True)
    semester_num = models.PositiveSmallIntegerField()
    group_id = models.ForeignKey(Group, on_delete=models.PROTECT, db_column='group_id')

    def set_semester_num(self, semester_num):
        self.semester_num = semester_num

    def set_group_id(self, group_id):
        self.group_id = group_id

    def __str__(self):
        return f'{self.group_id} {self.semester_num}'

    class Meta:
        db_table = 'group_semesters'
        constraints = [
            models.CheckConstraint(
                check=models.Q(semester_num__lte=10),
                name="%(app_label)s_%(class)s_semester_num_lte_10"
            ),
            models.UniqueConstraint(fields=['group_id', 'semester_num'], name='group_semester_num_unique')
        ]


class GroupMember(models.Model):
    group_member_id = models.AutoField(primary_key=True)
    group_semester_id = models.ForeignKey(GroupSemester, on_delete=models.PROTECT, db_column='group_semester_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'group_members'

    def __str__(self):
        return f'{self.group_member_id}'


class Curriculum(models.Model):
    curriculum_id = models.AutoField(primary_key=True)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.PROTECT, db_column='discipline_id')
    group_semester_id = models.ForeignKey(GroupSemester, on_delete=models.PROTECT, db_column='group_semester_id')

    def set_discipline(self, discipline_id):
        self.discipline_id = discipline_id

    def set_group_semester(self, group_semester_id):
        self.group_semester_id = group_semester_id

    def __str__(self):
        return f'{self.discipline_id.name} {self.group_semester_id.group_id.name}'


    # def clean_discipline_id(self):
    #     cd = self.cleaned_data.get('discipline_id')
    #     print(cd)
    #     return cd
    #
    # def clean(self):
    #     self.clean_discipline_id()


    # def validate_unique_curriculum(self):
    #     print(Curriculum.objects.filter(discipline_id_id=self.discipline_id, group_semester_id_id=self.group_semester_id))
    #     if Curriculum.objects.filter(
    #             discipline_id_id=self.discipline_id,
    #             group_semester_id_id=self.group_semester_id).exists():
    #         raise ValidationError({'discipline_id': ['Name must be unique per site.', ]})

    # def save(self, *args, **kwargs):
    #     self.validate_unique_curriculum()
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = 'curriculums'
        constraints = [
            models.UniqueConstraint(fields=['discipline_id', 'group_semester_id'], name='discipline_group_sem_unique')
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

    def __str__(self):
        return f'{self.curriculum_id} {self.get_lesson_type_display()}'

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
    name = models.CharField(max_length=64, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.name} {self.start_time} {self.end_time}'

    class Meta:
        db_table = 'lessons_time'
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name='check_start_time',
            ),
        ]

    def get_absolute_url(self):
        return reverse('account:lesson_time_edit',
                       args=[self.lesson_id])

    def get_delete_url(self):
        return reverse('account:lesson_time_delete',
                       args=[self.lesson_id])


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=8, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.number}'

    class Meta:
        db_table = 'classroom'

    def get_absolute_url(self):
        return reverse('account:classroom_edit',
                       args=[self.classroom_id])

    def get_delete_url(self):
        return reverse('account:classroom_delete',
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
    lessons_time_id = models.ForeignKey(LessonTime, on_delete=models.PROTECT, db_column='lessons_time_id')
    classroom_id = models.ForeignKey(Classroom, on_delete=models.PROTECT, db_column='classroom_id')
    curriculum_lesson_id = models.ForeignKey(CurriculumLesson, on_delete=models.PROTECT,
                                             db_column='curriculum_lesson_id')

    class Meta:
        db_table = 'tt_lesson'


class Homework(models.Model):
    hw_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2048)
    day_given = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_given', db_column='day_given')
    day_due = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_due', db_column='day_due')
    hw_type = models.PositiveSmallIntegerField()
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
        db_table = 'file'


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
    coefficient_id = models.AutoField(primary_key=True)
    coef_num = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=64)

    class Meta:
        db_table = 'coefficient'


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    scale_5 = models.PositiveSmallIntegerField()
    scale_word = models.CharField(max_length=32)
    scale_100 = models.PositiveSmallIntegerField()
    scale_letter = models.CharField(max_length=1)
    coef_num = models.PositiveSmallIntegerField()
    coef_description = models.CharField(max_length=64)
    coefficient_id = models.ForeignKey(Coefficient, on_delete=models.PROTECT, db_column='coefficient_id')
    progress_id = models.ForeignKey(StudentProgress, on_delete=models.PROTECT, db_column='progress_id')

    class Meta:
        db_table = 'grade'
