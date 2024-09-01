"""
Forms for account app.
"""

from django import forms
from django.contrib.auth import get_user_model
from formset.widgets import DateCalendar
from django.forms.utils import ErrorList, ErrorDict
from timetable.models import Student, Tutor, Group, Discipline, Classroom, LessonTime, GroupSemester, GroupMember, Curriculum, CurriculumLesson, TypesOfLesson, TTLesson

from django.core.exceptions import ValidationError

User = get_user_model()

USER_TYPES = (
    ("STD", "Студент"),
    ("TUT", "Преподаватель"),
    ("ALL", "Все")
)


class LoginForm(forms.Form):
    """
    Form for user data to log in.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class StudentAdditionalForm(forms.ModelForm):
    """
    Form for additional student information.
    """
    date_of_birth = forms.DateField(label='Дата рождения', input_formats=['%d.%m.%Y'], required=False,
                                    widget=forms.TextInput(attrs={
                                        'class': 'datepicker'
                                    }))

    class Meta:
        """
        Metaclass for student additional information form.
        """
        model = Student
        fields = ['date_of_birth']

    def __init__(self, required, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'] = forms.DateField(label='Дата рождения', input_formats=['%d.%m.%Y'], required=required,
                                    widget=forms.TextInput(attrs={
                                        'class': 'datepicker'
                                    }))


class TutorAdditionalForm(forms.ModelForm):
    """
    Form for additional tutor information.
    """
    # date_of_birth = forms.DateField(label='Дата рождения', input_formats=['%d.%m.%Y'], required=False,
    #                                 widget=forms.TextInput(attrs={
    #                                     'class': 'datepicker'
    #                                 }))

    class Meta:
        """
        Metaclass for tutor additional information form.
        """
        model = Tutor
        fields = ['date_of_birth']

    def __init__(self, required, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'] = forms.DateField(label='Дата рождения', input_formats=['%d.%m.%Y'], required=required,
                                    widget=forms.TextInput(attrs={
                                        'class': 'datepicker'
                                    }))


    # def change_required(self, required):
    #     self.date_of_birth = forms.DateField(label='Дата рождения', input_formats=['%d.%m.%Y'], required=required,
    #                                 widget=forms.TextInput(attrs={
    #                                     'class': 'datepicker'
    #                                 }))


class UserRegistrationForm(forms.ModelForm):
    """
    Form for user data to register.
    """
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Отчество')
    username = forms.CharField(label='Логин', required=True, help_text='1112')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    # is_student = forms.ChoiceField(choices=USER_TYPES
    is_student = forms.BooleanField(label='Студент', widget=forms.CheckboxInput, required=False, initial=False)
    is_tutor = forms.BooleanField(label='Преподаватель', widget=forms.CheckboxInput, required=False, initial=False)

    class Meta:
        """
        Metaclass for user registration form.
        """
        model = User
        fields = ['last_name', 'first_name', 'second_name', 'username', 'first_name', 'email', 'password', 'password2',
                  'is_student', 'is_tutor']

    class Media:
        js = ('js/user_form.js',)

    def clean_password2(self):
        """
        Checks the first and the second user's attempts to enter a password.
        :return: user's password
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Введенные пароли не совпадают')
        return cd['password2']

    # def clean(self):
    #     print("Hey")
    #     cleaned_data = super().clean()
    #     self._errors = ErrorDict()
    #     print(self.data.getlist('std-date_of_birth', None))
    #
    #     if self.data['is_student']:
    #         if self.data.getlist('std-date_of_birth', None)[0] == '':
    #             self.add_error('std-date_of_birth', ["Поле должно быть заполнено.", ])
    #
    #     return cleaned_data


class UserEditForm(forms.ModelForm):
    """
    Form for user data to edit.
    """
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Отчество')
    username = forms.CharField(label='Логин', required=True, help_text='1112')

    class Meta:
        """
        Metaclass for user edit form.
        """
        model = User
        fields = ['last_name', 'first_name', 'second_name', 'username', 'first_name', 'email']

    class Media:
        js = ('js/user_edit_form.js',)

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        return cleaned_data



class GroupRegisterForm(forms.ModelForm):
    name = forms.CharField(label='Название группы')

    class Meta:
        model = Group
        fields = ['name']


class DisciplineRegisterForm(forms.ModelForm):
    name = forms.CharField(label='Название дисциплины')
    description = forms.CharField(label='Описание дисциплины', required=False)

    class Meta:
        model = Discipline
        fields = ['name', 'description']


class ClassroomRegisterForm(forms.ModelForm):
    number = forms.CharField(label='Номер аудитории')
    description = forms.CharField(label='Описание аудитории', required=False)

    class Meta:
        model = Classroom
        fields = ['number', 'description']


class LessonTimeRegisterForm(forms.ModelForm):
    name = forms.CharField(label='Название урока')
    start_time = forms.TimeField(label='Начало занятия',
                                 widget=forms.TextInput(attrs={
                                     'class': 'timepicker'
                                 })
                                 )
    end_time = forms.TimeField(label='Окончание занятия',
                               widget=forms.TextInput(attrs={
                                   'class': 'timepicker'
                               })
                               )

    class Meta:
        model = LessonTime
        fields = ['name', 'start_time', 'end_time']

    class Media:
        js = ('js/time_form.js',)


class LessonTimeEditForm(forms.ModelForm):
    name = forms.CharField(label='Название времени занятия')
    start_time = forms.TimeField(label='Начало занятия',
                                 widget=forms.TextInput(attrs={
                                     'class': 'timepicker'
                                 })
                                 )
    end_time = forms.TimeField(label='Окончание занятия',
                               widget=forms.TextInput(attrs={
                                   'class': 'timepicker'
                               })
                               )

    class Meta:
        model = LessonTime
        fields = ['name', 'start_time', 'end_time']

    class Media:
        js = ('js/time_form.js',)


class GroupSemesterRegisterForm(forms.ModelForm):
    semester_num = forms.IntegerField(label='Номер семестра')
    # group_id = forms.IntegerField(label='Номер uheggs')
    group_id = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label='-----', label='Группа')

    class Meta:
        model = GroupSemester
        fields = ['group_id', 'semester_num']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semester_num'].queryset = GroupSemester.objects.none()

    class Media:
        js = ('js/group_semester_form.js',)


class GroupMemberRegisterForm(forms.ModelForm):
    group_semesters = forms.ModelChoiceField(GroupSemester.objects.all(), empty_label='-----', label='Группа')
    student_id = forms.ModelChoiceField(Student.objects.all(), empty_label='-----', label='Студент')

    def __init__(self, *args, **kwargs):
        super(GroupMemberRegisterForm, self).__init__(*args, **kwargs)
        self.fields['group_semesters'].widget.attrs['class'] = 'choice_input'
        self.fields['student_id'].widget.attrs['class'] = 'choice_input'

    class Meta:
        model = GroupMember
        fields = ['student_id', 'group_semesters']


class CurriculumRegisterForm(forms.ModelForm):
    discipline_id = forms.ModelChoiceField(Discipline.objects.all(), empty_label='-----', label='Дисциплины')
    group_semester_id = forms.ModelChoiceField(GroupSemester.objects.all(), empty_label='-----', label='Группы')

    def __init__(self, *args, **kwargs):
        super(CurriculumRegisterForm, self).__init__(*args, **kwargs)
        self.fields['discipline_id'].widget.attrs['class'] = 'choice_input'
        self.fields['group_semester_id'].widget.attrs['class'] = 'choice_input'

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

        group_semesters = self.data.getlist('group_semester_id', None)
        if group_semesters is not None:
            group_semesters_without_blank = list(filter(lambda x: x != '', group_semesters))
            print(group_semesters_without_blank)
            if len(group_semesters_without_blank) != len(set(group_semesters_without_blank)):
                self.add_error('group_semester_id', ["Поле не должно содержать повторяющихся значений.", ])
            for grsem in group_semesters:
                print("***")
                if grsem == '':
                    self.add_error('group_semester_id', ["Обязательное поле.", ])
                    break
            for grsem in group_semesters:
                print("*****")
                if grsem != '' and not GroupSemester.objects.filter(group_semester_id=grsem).exists():
                    self.add_error('group_semester_id',
                                   ["Выберите корректный вариант. Вашего варианта нет среди допустимых значений.", ])
                    break

        return cleaned_data

    class Meta:
        model = Curriculum
        fields = ['group_semester_id', 'discipline_id']


class CurriculumLessonRegisterForm(forms.ModelForm):
    lesson_type = forms.ChoiceField(label="Тип урока", choices=TypesOfLesson.choices)
    duration = forms.IntegerField(label="Продолжительность")
    curriculum_id = forms.ModelChoiceField(Curriculum.objects.all(), empty_label='-----', label='План занятий')
    # tutors = Tutor.objects.all()
    tutor_id = forms.ModelChoiceField(Tutor.objects.all(), empty_label='-----', label='Преподаватель')

    def __init__(self, *args, **kwargs):
        super(CurriculumLessonRegisterForm, self).__init__(*args, **kwargs)
        self.fields['lesson_type'].widget.attrs['class'] = 'choice_input'
        self.fields['curriculum_id'].widget.attrs['class'] = 'choice_input'
        self.fields['tutor_id'].widget.attrs['class'] = 'choice_input'

    def set_initial_curriculum_ids(self, objects):
        self.fields['curriculum_id'].queryset = objects

    class Meta:
        model = CurriculumLesson
        fields = ['lesson_type', 'duration', 'curriculum_id', 'tutor_id' ]


class TTLessonRegisterForm(forms.ModelForm):
    date = forms.DateField(label='Дата занятия', input_formats=['%d.%m.%Y'], required=False,
                      widget=forms.TextInput(attrs={
                          'class': 'datepicker'
                      }))
    day_name = forms.ChoiceField(label="День недели", choices=TTLesson.DAY_OF_WEEK_CHOICES)
    week_type = forms.ChoiceField(label="Тип недели", choices=TTLesson.TYPE_OF_WEEK_CHOICES)
    lessons_time_id = forms.ModelChoiceField(LessonTime.objects.all(), empty_label='-----', label='Время занятия')
    classroom_id = forms.ModelChoiceField(Classroom.objects.all(), empty_label='-----', label='Аудитория')
    curriculum_lesson_id = forms.ModelChoiceField(CurriculumLesson.objects.all(), empty_label='-----', label='Предмет')

    def __init__(self, *args, **kwargs):
        super(TTLessonRegisterForm, self).__init__(*args, **kwargs)
        self.fields['day_name'].widget.attrs['class'] = 'choice_input'
        self.fields['week_type'].widget.attrs['class'] = 'choice_input'
        self.fields['lessons_time_id'].widget.attrs['class'] = 'choice_input'
        self.fields['classroom_id'].widget.attrs['class'] = 'choice_input'
        self.fields['curriculum_lesson_id'].widget.attrs['class'] = 'choice_input'

    class Meta:
        model = TTLesson
        fields = ['date', 'day_name', 'week_type', 'lessons_time_id', 'classroom_id', 'curriculum_lesson_id']
