"""
URL configuration for progress app.
"""

from django.urls import path, re_path, register_converter
from . import views
from .converters import DateConverter

app_name = 'progress'

register_converter(DateConverter, 'date')

urlpatterns = [
    path('student_attendance/choose', views.student_attendance_choose, name='student_attendance_choose'),
    path('student_attendance/edit/<int:curriculum_lesson_id>', views.student_attendance_edit, name='student_attendance_edit')
]
