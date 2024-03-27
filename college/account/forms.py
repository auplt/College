"""
Forms for account app.
"""

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    """
    Form for user data to log in.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
    Form for user data to register.
    """
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        """
        Metaclass for user registration form.
        """
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        """
        Checks the first and the second user's attempts to enter a password.
        :return: user's password
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Введенные пароли не совпадают')
        return cd['password2']
