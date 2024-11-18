"""
Models for group app.
"""

from django.db import models
from django.urls import reverse

from user.models import Student, Tutor


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'groups'

    def get_absolute_url(self):
        return reverse('group:group_details',
                       args=[self.group_id])

    def get_edit_url(self):
        return reverse('group:group_edit',
                       args=[self.group_id])

    def get_delete_url(self):
        return reverse('group:group_delete',
                       args=[self.group_id])


class GroupSemester(models.Model):
    group_semester_id = models.AutoField(primary_key=True)
    semester_num = models.PositiveSmallIntegerField()
    group_id = models.ForeignKey(Group, on_delete=models.PROTECT, db_column='group_id')

    def set_semester_num(self, semester_num):
        self.semester_num = semester_num

    def set_group_id(self, group_id):
        self.group_id = group_id

    def __str__(self):
        return f'{self.group_id} сем. {self.semester_num}'

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
        constraints = [
            models.UniqueConstraint(fields=['group_semester_id', 'student_id'],
                                    name='group_members_group_semester_student_unique')
        ]

    def __str__(self):
        return f'{self.group_member_id}'
