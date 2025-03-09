"""
Forms for progress app.
"""

from django import forms

from user.models import Student
from timetable.models import TTLesson
from .models import Homework, TypesOfHomework, File

class HomeworkRegisterForm(forms.ModelForm):
    description = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Описание'}))
    # hw_type = forms.ModelChoiceField(TypesOfHomework.choices, empty_label='Тип домашнего задания', label=False)
    day_due = forms.ModelChoiceField(TTLesson.objects.all(), empty_label='Занятие', label=False)
    day_given = forms.ModelChoiceField(TTLesson.objects.all(), empty_label='Задано на занятие', label=False)
    file_id = forms.ModelChoiceField(File.objects.all(), empty_label='Файл', label=False, required=False)
    student_id = forms.ModelChoiceField(Student.objects.all(), empty_label='Студент', label=False, required=False)

    def __init__(self, *args, **kwargs):
        super(HomeworkRegisterForm, self).__init__(*args, **kwargs)
        self.fields['hw_type'].widget.attrs['class'] = 'choice_input'
        self.fields['day_due'].widget.attrs['class'] = 'choice_input'
        self.fields['day_given'].widget.attrs['class'] = 'choice_input'
        self.fields['file_id'].widget.attrs['class'] = 'choice_input'
        self.fields['student_id'].widget.attrs['class'] = 'choice_input'
    
    class Meta:
        model = Homework
        fields = ['description', 'hw_type', 'day_due', 'day_given', 'file_id', 'student_id']


