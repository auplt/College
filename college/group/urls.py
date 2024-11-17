"""
URL configuration for group app.
"""

from django.urls import path, re_path, register_converter
from . import views
from timetable.converters import DateConverter

app_name = 'group'

register_converter(DateConverter, 'date')

urlpatterns = [
    path('list/', views.group_list, name='group_list'),
    re_path(r'details/(?P<group_id>\d+)?/?(?P<week>(True|False))?&?(?P<day_delta>\d+)?/?$', views.group_details,
            name='group_details'),
    path('register', views.group_register, name='group_register'),
    path('edit/<int:group_id>', views.group_edit, name='group_edit'),
    path('delete/<int:group_id>', views.group_delete, name='group_delete'),

    re_path(r'group_semester/register/?(?P<group_id>\d+)?/?$', views.group_semester_register,
            name='group_semester_register'),
    path('group_semester/register', views.group_semester_register, name='group_semester_register'),
    re_path(r'group_semester/delete/?(?P<group_id>\d+)?&?(?P<semester_num>\d+)?/?', views.group_semester_delete,
            name='group_semester_delete'),

    re_path(r'group_member/register/?(?P<group_id>\d+)?&?(?P<semester_num>\d+)?/?$', views.group_member_register,
            name='group_member_register'),
    re_path(r'group_member/register/?(?P<student_id>\d+)?/?$', views.group_member_register,
            name='group_member_register'),
    re_path(r'group_member/register/?(?P<group_id>\d+)?/?$', views.group_member_register, name='group_member_register'),
    path('group_member/register', views.group_member_register, name='group_member_register'),
    path('group_member/delete/<int:group_member_id>', views.group_member_delete, name='group_member_delete'),

    path('group_semester/ajax/load_max_semester', views.load_max_semester, name='ajax_load_max_semester')
]
