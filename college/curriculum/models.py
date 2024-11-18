"""
Models for curriculum app.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from user.models import Tutor
from group.models import GroupSemester


class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'disciplines'

    def get_absolute_url(self):
        return reverse('curriculum:discipline_details',
                       args=[self.discipline_id])

    def get_edit_url(self):
        return reverse('curriculum:discipline_edit',
                       args=[self.discipline_id])

    def get_delete_url(self):
        return reverse('curriculum:discipline_delete',
                       args=[self.discipline_id])


class Curriculum(models.Model):
    curriculum_id = models.AutoField(primary_key=True)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.PROTECT, db_column='discipline_id')
    group_semester_id = models.ForeignKey(GroupSemester, on_delete=models.PROTECT, db_column='group_semester_id')

    def set_discipline(self, discipline_id):
        self.discipline_id = discipline_id

    def set_group_semester(self, group_semester_id):
        self.group_semester_id = group_semester_id

    def __str__(self):
        return f'{self.discipline_id} гр. {self.group_semester_id}'

    class Meta:
        db_table = 'curriculums'
        constraints = [
            models.UniqueConstraint(fields=['discipline_id', 'group_semester_id'], name='discipline_group_sem_unique')
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
        return f'{self.curriculum_id} {self.get_lesson_type_display()} Преп. {self.tutor_id}'

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
            ),
            models.UniqueConstraint(fields=['curriculum_id', 'tutor_id', 'lesson_type'],
                                    name='curriculum_lessons_curriculum_tutor_les_type_unique')
        ]
