"""
URL configuration for account app.
"""
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginView.as_view(), name='login'),


    path('', views.dashboard, name='dashboard'),

    path('user/', views.user_list, name='user_list'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/details/<int:id>', views.user_details, name='user_details'),
    path('user/edit/<int:id>', views.user_edit, name='user_edit'),
    path('user/delete/<int:id>', views.user_delete, name='user_delete'),
    path('user/delete/<int:id>/tutor', views.user_delete_tutor, name='user_delete_tutor'),
    path('user/delete/<int:id>/student', views.user_delete_student, name='user_delete_student'),

    # path('lgout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='user_logout'),
    path('group/details/<int:group_id>', views.group_details, name='group_details'),
    path('register_group', views.register_group, name='register_group'),

    path('discipline/', views.discipline_list, name='discipline_list'),
    path('discipline/register', views.discipline_register, name='discipline_register'),
    path('discipline/details/<int:discipline_id>', views.discipline_details, name='discipline_details'),
    path('discipline/edit/<int:discipline_id>', views.discipline_edit, name='discipline_edit'),
    path('discipline/delete/<int:discipline_id>', views.discipline_delete, name='discipline_delete'),

    path('classroom/', views.classroom_list, name='classroom_list'),
    path('classroom/register', views.classroom_register, name='classroom_register'),
    path('classroom/details/<int:classroom_id>', views.classroom_details, name='classroom_details'),
    path('classroom/edit/<int:classroom_id>', views.classroom_edit, name='classroom_edit'),
    path('classroom/delete/<int:classroom_id>', views.classroom_delete, name='classroom_delete'),

    path('lesson_time/', views.lesson_time_list, name='lesson_time_list'),
    path('lesson_time/register', views.lesson_time_register, name='lesson_time_register'),
    path('lesson_time/details/<int:lesson_id>', views.lesson_time_details, name='lesson_time_details'),
    path('lesson_time/edit/<int:lesson_id>', views.lesson_time_edit, name='lesson_time_edit'),
    path('lesson_time/delete/<int:lesson_id>', views.lesson_time_delete, name='lesson_time_delete'),

    path('group_semester/register', views.register_group_semester, name='register_group_semester'),

    path(r'group_member/register/?(?P<student_id>\d+)?/?$', views.group_member_register, name='group_member_register'),
    path('group_member/register', views.group_member_register, name='group_member_register'),

    # path(r'^curriculum/register/?(', views.curriculum_register, name='curriculum_register'),
    path(r'curriculum/register/?(?P<discipline_id>\d+)?/?$', views.curriculum_register, name='curriculum_register'),
    path('curriculum/register/', views.curriculum_register, name='curriculum_register'),

    path(r'curriculum_lesson/register/?(?P<tutor_id>\d+)?/?$', views.curriculum_lesson_register, name='curriculum_lesson_register'),
    path(r'curriculum_lesson/register/?(?P<discipline_id>\d+)?/?$', views.curriculum_lesson_register, name='curriculum_lesson_register'),
    path('curriculum_lesson/register/', views.curriculum_lesson_register, name='curriculum_lesson_register'),
    path('tt_lesson/register/', views.register_tt_lesson, name='tt_lesson'),

    path('group_semester/ajax/load_max_semester', views.load_max_semester, name='ajax_load_max_semester')

               ]

