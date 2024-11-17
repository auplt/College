"""
Forms for curriculum app.
"""

from django import forms
from django.forms.utils import ErrorDict
from timetable.models import Student, Tutor, Group, Discipline, Classroom, LessonTime, GroupSemester, GroupMember, \
    Curriculum, CurriculumLesson, TypesOfLesson, TTLesson


# DISCIPLINE FORMS

class DisciplineRegisterForm(forms.ModelForm):
    name = forms.CharField(label=False,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Название'
                           }))
    description = forms.CharField(label=False, required=False,
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'Описание'
                                  }))

    class Meta:
        model = Discipline
        fields = ['name', 'description']


# CURRICULUM FORMS

class CurriculumRegisterForm(forms.ModelForm):
    discipline_id = forms.ModelChoiceField(Discipline.objects.all().order_by('name'), empty_label='Дисциплины',
                                           label=False)
    group_semester_id = forms.ModelChoiceField(GroupSemester.objects.all().order_by('-semester_num', 'group_id__name'),
                                               empty_label='Группы', label=False)

    def __init__(self, *args, **kwargs):
        super(CurriculumRegisterForm, self).__init__(*args, **kwargs)
        self.fields['discipline_id'].widget.attrs['class'] = 'choice_input'
        self.fields['group_semester_id'].widget.attrs['class'] = 'choice_input'

    def set_initial_group_semester_ids(self, objects):
        self.fields['group_semester_id'].queryset = objects

    def clean(self):
        cleaned_data = super().clean()
        self._errors = ErrorDict()

        disciplines = self.data.getlist('discipline_id', None)
        if disciplines is not None:
            disciplines_without_blank = list(filter(lambda x: x != '', disciplines))
            print(disciplines_without_blank)
            if len(disciplines_without_blank) != len(set(disciplines_without_blank)):
                self.add_error('discipline_id', ["Поле не должно содержать повторяющихся значений.", ])
            for disc in disciplines:
                print("***")
                if disc == '':
                    self.add_error('discipline_id', ["Обязательное поле.", ])
                    break
            for disc in disciplines:
                print("*****")
                if disc != '' and not Discipline.objects.filter(discipline_id=disc).exists():
                    self.add_error('discipline_id',
                                   ["Выберите корректный вариант. Вашего варианта нет среди допустимых значений.", ])
                    break

        group_semester_id = self.data.getlist('group_semester_id', None)
        if group_semester_id is not None:
            group_semester_id_without_blank = list(filter(lambda x: x != '', group_semester_id))
            print(group_semester_id_without_blank)
            if len(group_semester_id_without_blank) != len(set(group_semester_id_without_blank)):
                self.add_error('group_semester_id', ["Поле не должно содержать повторяющихся значений.", ])
            for grsem in group_semester_id:
                print("***")
                if grsem == '':
                    self.add_error('group_semester_id', ["Обязательное поле.", ])
                    break
            for grsem in group_semester_id:
                print("*****")
                if grsem != '' and not GroupSemester.objects.filter(group_semester_id=grsem).exists():
                    self.add_error('group_semester_id',
                                   ["Выберите корректный вариант. Вашего варианта нет среди допустимых значений.", ])
                    break

        return cleaned_data

    class Meta:
        model = Curriculum
        fields = ['group_semester_id', 'discipline_id']


# CURRICULUM LESSON FORMS

class CurriculumLessonRegisterForm(forms.ModelForm):
    lesson_type = forms.ChoiceField(label=False, choices=TypesOfLesson.choices)
    duration = forms.IntegerField(label=False,
                                  widget=forms.NumberInput(attrs={
                                      'placeholder': 'Продолжительность'
                                  }))
    curriculum_id = forms.ModelChoiceField(Curriculum.objects.all(), empty_label='План занятий', label=False)
    # tutors = Tutor.objects.all()
    tutor_id = forms.ModelChoiceField(Tutor.objects.all(), empty_label='Преподаватель', label=False)

    def __init__(self, *args, **kwargs):
        super(CurriculumLessonRegisterForm, self).__init__(*args, **kwargs)
        self.fields['lesson_type'].widget.attrs['class'] = 'choice_input'
        self.fields['curriculum_id'].widget.attrs['class'] = 'choice_input'
        self.fields['tutor_id'].widget.attrs['class'] = 'choice_input'

    def set_initial_curriculum_ids(self, objects):
        self.fields['curriculum_id'].queryset = objects

    class Meta:
        model = CurriculumLesson
        fields = ['lesson_type', 'duration', 'curriculum_id', 'tutor_id']
