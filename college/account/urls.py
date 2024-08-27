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
    path('register/', views.register, name='register'),
    # path('lgout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='user_logout'),
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
    path('group_member/register', views.register_group_member, name='register_group_member'),

    # path(r'^curriculum/register/?(', views.curriculum_register, name='curriculum_register'),
    path(r'curriculum/register/?(?P<discipline_id>\d+)?/?$', views.curriculum_register, name='curriculum_register'),
    path('curriculum/register/', views.curriculum_register, name='curriculum_register'),

    path('curriculum_lesson/register/', views.register_curriculum_lesson, name='curriculum_lesson'),
    path('tt_lesson/register/', views.register_tt_lesson, name='tt_lesson'),

    path('group_semester/ajax/load_max_semester', views.load_max_semester, name='ajax_load_max_semester')

               ]

