"""
Forms for account app.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from formset.widgets import DateCalendar
from django.forms.utils import ErrorList, ErrorDict
from django.utils.translation import gettext_lazy as _
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
    error_messages = {
        "invalid_login": _(
            "Имя пользователя или пароль неверны. Повторите попытку входа"
        ),
        "inactive": _("Аккаунт неактивен"),
    }

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

    # class Media:
    #     js = ('js/user_form.js',)

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

    # class Media:
    #     js = ('js/user_edit_form.js',)

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        return cleaned_data














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
#         js = ('js/lesson_time_form.js',)







