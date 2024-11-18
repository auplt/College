"""
Configuration for user app models on admin panel.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Student
from .models import CustomUser


admin.site.register(Student)
admin.site.register(CustomUser, UserAdmin)
