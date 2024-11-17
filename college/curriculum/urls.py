"""
URL configuration for curriculum app.
"""
from django.urls import path, re_path
from . import views


app_name = 'curriculum'

urlpatterns = [
    path('discipline/', views.discipline_list, name='discipline_list'),
    path('discipline/register', views.discipline_register, name='discipline_register'),
    path('discipline/details/<int:discipline_id>', views.discipline_details, name='discipline_details'),
    path('discipline/edit/<int:discipline_id>', views.discipline_edit, name='discipline_edit'),
    path('discipline/delete/<int:discipline_id>', views.discipline_delete, name='discipline_delete'),

    re_path(r'curriculum/register/?(?P<group_id>\d+)?&?(?P<semester_num>\d+)?/?', views.curriculum_register,
            name='curriculum_register'),
    re_path(r'curriculum/register/?(?P<group_id>\d+)?/?$', views.curriculum_register, name='curriculum_register'),
    re_path(r'curriculum/register/?(?P<discipline_id>\d+)?/?$', views.curriculum_register, name='curriculum_register'),
    path('curriculum/register/', views.curriculum_register, name='curriculum_register'),
    path('curriculum/delete/<int:curriculum_id>/', views.curriculum_delete,
         name='curriculum_delete'),
    re_path(r'curriculum/delete/?(?P<discipline_id>\d+)?&?(?P<group_semester_id>\d+)?/?', views.curriculum_delete,
            name='curriculum_delete_params'),

    path('curriculum_lesson/details/groups/<int:group_id>', views.curriculum_lesson_group_details,
         name='curriculum_lesson_group_details'),
    re_path(r'curriculum_lesson/register/?(?P<group_id>\d+)?&?(?P<group_semester_id>\d+)?&?(?P<discipline_id>\d+)?/?',
            views.curriculum_lesson_register,
            name='curriculum_lesson_register'),
    re_path(r'curriculum_lesson/register/?(?P<tutor_id>\d+)?/?$', views.curriculum_lesson_register,
            name='curriculum_lesson_register'),
    re_path(r'curriculum_lesson/register/?(?P<discipline_id>\d+)?/?$', views.curriculum_lesson_register,
            name='curriculum_lesson_register'),
    path('curriculum_lesson/register/', views.curriculum_lesson_register, name='curriculum_lesson_register'),
    path('curriculum_lesson/edit/<int:curriculum_lesson_id>', views.curriculum_lesson_edit,
         name='curriculum_lesson_edit'),
    path('curriculum_lesson/delete/<int:curriculum_lesson_id>', views.curriculum_lesson_delete,
         name='curriculum_lesson_delete')
]
