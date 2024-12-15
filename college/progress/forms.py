"""
Forms for progress app.
"""

from django import forms

from curriculum.models import Curriculum
from timetable.models import TTLesson
from .models import FinalGrade, File, Homework, StudentAttendance, Coefficient, Grade, StudentProgress


# STUDENT ATTENDANCE FORMS
class AttendanceChooseForm(forms.ModelForm):
    curriculum_id = forms.ModelChoiceField(Curriculum.objects.all(), empty_label='Занятие', label=False)

    class Meta:
        model = StudentAttendance
        fields = ['is_present']

