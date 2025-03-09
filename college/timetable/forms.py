"""
Forms for timetable app.
"""

from django import forms

from curriculum.models import CurriculumLesson
from .models import Classroom, LessonTime, TTLesson


# CLASSROOM FORMS
class ClassroomRegisterForm(forms.ModelForm):
    number = forms.CharField(label=False,
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Номер'
                             }))
    description = forms.CharField(label=False,
                                  required=False,
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'Описание'
                                  }))

    class Meta:
        model = Classroom
        fields = ['number', 'description']


# LESSON TIME FORMS
class LessonTimeRegisterForm(forms.ModelForm):
    name = forms.CharField(label=False,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Название'
                           })
                           )
    start_time = forms.TimeField(label=False,
                                 widget=forms.TimeInput(attrs={
                                     'class': 'timepicker',
                                     'placeholder': 'Начало занятия'
                                 }, format='%H:%M')
                                 )
    end_time = forms.TimeField(label=False,
                               widget=forms.TimeInput(attrs={
                                   'class': 'timepicker',
                                   'placeholder': 'Окончание занятия'
                               }, format='%H:%M')
                               )

    class Meta:
        model = LessonTime
        fields = ['name', 'start_time', 'end_time']


# TIMETABLE LESSON FORMS
class TTLessonRegisterForm(forms.ModelForm):
    date = forms.DateField(label=False, input_formats=['%d.%m.%Y'], required=True,
                           widget=forms.TextInput(attrs={
                               'class': 'datepicker',
                               'placeholder': 'Дата занятия'
                           }))
    # day_name = forms.ChoiceField(label="День недели", choices=TTLesson.DAY_OF_WEEK_CHOICES)
    # week_type = forms.ChoiceField(label="Тип недели", choices=TTLesson.TYPE_OF_WEEK_CHOICES)
    lesson_time_id = forms.ModelChoiceField(LessonTime.objects.all(), empty_label='Время занятия', label=False)
    classroom_id = forms.ModelChoiceField(Classroom.objects.all(), empty_label='Аудитория', label=False)
    curriculum_lesson_id = forms.ModelChoiceField(CurriculumLesson.objects.all(), empty_label='Предмет', label=False)

    def __init__(self, *args, **kwargs):
        super(TTLessonRegisterForm, self).__init__(*args, **kwargs)
        # self.fields['week_type'].widget.attrs['class'] = 'choice_input'
        self.fields['lesson_time_id'].widget.attrs['class'] = 'choice_input'
        self.fields['classroom_id'].widget.attrs['class'] = 'choice_input'
        self.fields['curriculum_lesson_id'].widget.attrs['class'] = 'choice_input'

    def set_initial_curriculum_lesson_ids(self, objects):
        self.fields['curriculum_lesson_id'].queryset = objects

    class Meta:
        model = TTLesson
        fields = ['date', 'lesson_time_id', 'classroom_id', 'curriculum_lesson_id']
