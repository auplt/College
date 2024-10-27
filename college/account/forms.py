"""
Forms for account app.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from formset.widgets import DateCalendar
from django.forms.utils import ErrorList, ErrorDict
from timetable.models import Student, Tutor, Group, Discipline, Classroom, LessonTime, GroupSemester, GroupMember, \
    Curriculum, CurriculumLesson, TypesOfLesson, TTLesson

from django.core.exceptions import ValidationError

User = get_user_model()

USER_TYPES = (
    ("STD", "Студент"),
    ("TUT", "Преподаватель"),
    ("ALL", "Все")
)


class CustomAuthenticationForm(AuthenticationForm):
    """
    Form for user data to log in.
    """
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Логин'
    }))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль'
    }))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Электронная почта'
    }))


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'Старый пароль',
        "autofocus": True
    }))
    new_password1 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Пароль',
               "autocomplete": "new-password"}))
    new_password2 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Повторите пароль',
               "autocomplete": "new-password"}))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Пароль',
               "autocomplete": "new-password"}))
    new_password2 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Повторите пароль',
               "autocomplete": "new-password"}))


class StudentAdditionalForm(forms.ModelForm):
    """
    Form for additional student information.
    """
    date_of_birth = forms.DateField(label=False, input_formats=['%d.%m.%Y'], required=False,
                                    widget=forms.TextInput(attrs={
                                        'class': 'datepicker',
                                        'placeholder': 'Дата рождения'
                                    }))

    class Meta:
        """
        Metaclass for student additional information form.
        """
        model = Student
        fields = ['date_of_birth']

    def __init__(self, required, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'] = forms.DateField(label=False, input_formats=['%d.%m.%Y'],
                                                       required=required,
                                                       widget=forms.TextInput(attrs={
                                                           'class': 'datepicker',
                                                           'placeholder': 'Дата рождения'
                                                       }))


class TutorAdditionalForm(forms.ModelForm):
    """
    Form for additional tutor information.
    """
    date_of_birth = forms.DateField(label=False, input_formats=['%d.%m.%Y'], required=False,
                                    widget=forms.TextInput(attrs={
                                        'class': 'datepicker',
                                        'placeholder': 'Дата рождения'
                                    }))

    class Meta:
        """
        Metaclass for tutor additional information form.
        """
        model = Tutor
        fields = ['date_of_birth']

    def __init__(self, required, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'] = forms.DateField(label=False, input_formats=['%d.%m.%Y'],
                                                       required=required,
                                                       widget=forms.TextInput(attrs={
                                                           'class': 'datepicker',
                                                           'placeholder': 'Дата рождения'
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
    last_name = forms.CharField(label=False,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Фамилия'
                                }))
    first_name = forms.CharField(label=False,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Имя'
                                 }))
    second_name = forms.CharField(label=False,
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'Отчество'
                                  }))
    username = forms.CharField(label=False, required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Логин'
                               }))
    email = forms.EmailField(label=False, required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Электронная почта'
                             }))
    password = forms.CharField(label=False,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Пароль'
                               }))
    password2 = forms.CharField(label=False,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Повторите пароль'
                                }))
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

    def user_fields(self):
        # Set of invisible fields
        invisibles = [self.fields['is_student'], self.fields['is_tutor']]
        # Set of visible fields
        visibles = super(UserRegistrationForm, self).visible_fields()
        return [v for v in visibles if v.field not in invisibles]

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
    last_name = forms.CharField(label=False,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Фамилия'
                                }))
    first_name = forms.CharField(label=False,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Имя'
                                 }))
    second_name = forms.CharField(label=False,
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'Отчество'
                                  }))
    username = forms.CharField(label=False,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Логин'
                               }))
    email = forms.EmailField(label=False, required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Электронная почта'
                             }))

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
    name = forms.CharField(label=False,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Название'
                           }))

    class Meta:
        model = Group
        fields = ['name']


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


class LessonTimeRegisterForm(forms.ModelForm):
    name = forms.CharField(label=False,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Название'
                           })
                           )
    start_time = forms.TimeField(label=False,
                                 widget=forms.TextInput(attrs={
                                     'class': 'timepicker',
                                     'placeholder': 'Начало занятия'
                                 })
                                 )
    end_time = forms.TimeField(label=False,
                               widget=forms.TextInput(attrs={
                                   'class': 'timepicker',
                                   'placeholder': 'Окончание занятия'
                               })
                               )

    class Meta:
        model = LessonTime
        fields = ['name', 'start_time', 'end_time']

    class Media:
        js = ('js/time_form.js',)


# class LessonTimeEditForm(forms.ModelForm):
#     name = forms.CharField(label='Название времени занятия')
#     start_time = forms.TimeField(label='Начало занятия',
#                                  widget=forms.TextInput(attrs={
#                                      'class': 'timepicker'
#                                  })
#                                  )
#     end_time = forms.TimeField(label='Окончание занятия',
#                                widget=forms.TextInput(attrs={
#                                    'class': 'timepicker'
#                                })
#                                )
#
#     class Meta:
#         model = LessonTime
#         fields = ['name', 'start_time', 'end_time']
#
#     class Media:
#         js = ('js/time_form.js',)


class GroupSemesterRegisterForm(forms.ModelForm):
    semester_num = forms.IntegerField(label=False,
                                      widget=forms.NumberInput(attrs={
                                          'placeholder': 'Номер семестра'
                                      }))
    group_id = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label='Группа', label=False)

    class Meta:
        model = GroupSemester
        fields = ['group_id', 'semester_num']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_id'].widget.attrs['class'] = 'choice_input'
        self.fields['semester_num'].queryset = GroupSemester.objects.none()

    class Media:
        js = ('js/group_semester_form.js',)


class GroupMemberRegisterForm(forms.ModelForm):
    group_semester_id = forms.ModelChoiceField(GroupSemester.objects.all().order_by('-semester_num', 'group_id__name'),
                                               empty_label='Группа', label=False)
    student_id = forms.ModelChoiceField(
        Student.objects.all().order_by('user_id__last_name', 'user_id__first_name', 'user_id__second_name'),
        empty_label='Студент', label=False)

    def __init__(self, *args, **kwargs):
        super(GroupMemberRegisterForm, self).__init__(*args, **kwargs)
        self.fields['group_semester_id'].widget.attrs['class'] = 'choice_input'
        self.fields['student_id'].widget.attrs['class'] = 'choice_input'

    def set_initial_group_semester_ids(self, objects):
        self.fields['group_semester_id'].queryset = objects

    class Meta:
        model = GroupMember
        fields = ['student_id', 'group_semester_id']


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


class CurriculumLessonRegisterForm(forms.ModelForm):
    lesson_type = forms.ChoiceField(label=False, choices=TypesOfLesson.choices,
                                    widget=forms.NumberInput(attrs={
                                        'placeholder': 'Тип урока'
                                    }))
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
