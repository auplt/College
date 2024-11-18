"""
Models for user app.
"""

from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=128)
    last_name = models.CharField(_("last name"), max_length=128)
    second_name = models.CharField(_("second name"), max_length=128, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    def get_absolute_url(self):
        return reverse('user:user_details',
                       args=[self.id])

    def get_edit_url(self):
        return reverse('user:user_edit',
                       args=[self.id])

    def get_delete_url(self):
        return reverse('user:user_delete',
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
    user_id = models.OneToOneField(CustomUser, on_delete=models.PROTECT, db_column='user_id')

    def __str__(self):
        return f'{self.user_id.last_name} {self.user_id.first_name} {self.user_id.second_name}'

    class Meta:
        db_table = 'students'


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
    user_id = models.OneToOneField(CustomUser, on_delete=models.PROTECT, db_column='user_id')

    def __str__(self):
        return f'{self.user_id.last_name} {self.user_id.first_name} {self.user_id.second_name}'

    class Meta:
        db_table = 'tutors'
