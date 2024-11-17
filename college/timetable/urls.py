"""
URL configuration for timetable app.
"""

from django.urls import path,  re_path
from . import views

app_name = 'timetable'

urlpatterns = [
    re_path(r'tt_lesson/details/?(?P<date>[0-9]{2}.[0-9]{2}.[0-9]{4})?/?$', views.tt_lesson_details,
            name='tt_lesson_details'),
    re_path(
        r'tt_lesson/register/?(?P<date>[0-9]{2}.[0-9]{2}.[0-9]{4})?&?(?P<lesson_time_id>\d+)'
        r'?&?(?P<classroom_id>\d+)?&?(?P<group_id>\d+)?&?(?P<user_id>\d+)?/?$',
        views.tt_lesson_register, name='tt_lesson_register'),
    re_path(
        r'tt_lesson/details/edit/?(?P<date>[0-9]{2}.[0-9]{2}.[0-9]{4})?&?(?P<lesson_time_id>\d+)'
        r'?&?(P<tt_lesson_ids>\.*)?/?$',
        views.tt_lesson_details_edit, name='tt_lesson_details_edit'),
    path('tt_lesson/edit/<int:tt_lesson_id>', views.tt_lesson_edit, name='tt_lesson_edit'),
    path('tt_lesson/delete/<int:tt_lesson_id>', views.tt_lesson_delete, name='tt_lesson_delete')
]
