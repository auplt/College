"""
Forms for group app.
"""

from django import forms

from user.models import Student
from .models import Group, GroupMember, GroupSemester


# GROUP FORMS

class GroupRegisterForm(forms.ModelForm):
    name = forms.CharField(label=False,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Название'
                           }))

    class Meta:
        model = Group
        fields = ['name']


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
