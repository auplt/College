"""
URL configuration for account app.
"""
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginView.as_view(), name='login'),

    path('', views.dashboard, name='dashboard'),

    path('user/', views.user_list, name='user_list'),
    path('user/details/<int:id>', views.user_details, name='user_details'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/edit/<int:id>', views.user_edit, name='user_edit'),
    path('user/delete/<int:id>', views.user_delete, name='user_delete'),
    path('user/delete/<int:id>/tutor', views.user_delete_tutor, name='user_delete_tutor'),
    path('user/delete/<int:id>/student', views.user_delete_student, name='user_delete_student'),

    # path('lgout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='user_logout'),
    path('group/', views.group_list, name='group_list'),
    path('group/details/<int:group_id>', views.group_details, name='group_details'),
    path('group/register', views.group_register, name='group_register'),
    path('group/edit/<int:group_id>', views.group_edit, name='group_edit'),
    path('group/delete/<int:group_id>', views.group_delete, name='group_delete'),

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

    # path(r'^curriculum/register/?(', views.curriculum_register, name='curriculum_register'),
    re_path(r'curriculum/register/?(?P<group_id>\d+)?&?(?P<semester_num>\d+)?/?', views.curriculum_register,
            name='curriculum_register'),
    re_path(r'curriculum/register/?(?P<group_id>\d+)?/?$', views.curriculum_register, name='curriculum_register'),
    re_path(r'curriculum/register/?(?P<discipline_id>\d+)?/?$', views.curriculum_register, name='curriculum_register'),
    path('curriculum/register/', views.curriculum_register, name='curriculum_register'),
    re_path(r'curriculum/delete/?(?P<discipline_id>\d+)?&?(?P<group_semester_id>\d+)?/?', views.curriculum_delete,
            name='curriculum_delete'),

    path('curriculum_lesson/details/groups/<int:group_id>', views.curriculum_lesson_group_details, name='curriculum_lesson_group_details'),
    re_path(r'curriculum_lesson/register/?(?P<group_id>\d+)?&?(?P<group_semester_id>\d+)?&?(?P<discipline_id>\d+)?/?',
            views.curriculum_lesson_register,
            name='curriculum_lesson_register'),
    re_path(r'curriculum_lesson/register/?(?P<tutor_id>\d+)?/?$', views.curriculum_lesson_register,
            name='curriculum_lesson_register'),
    re_path(r'curriculum_lesson/register/?(?P<discipline_id>\d+)?/?$', views.curriculum_lesson_register,
            name='curriculum_lesson_register'),
    path('curriculum_lesson/register/', views.curriculum_lesson_register, name='curriculum_lesson_register'),
    path('curriculum_lesson/edit/<int:curriculum_lesson_id>', views.curriculum_lesson_edit, name='curriculum_lesson_edit'),
    path('curriculum_lesson/delete/<int:curriculum_lesson_id>', views.curriculum_lesson_delete, name='curriculum_lesson_delete'),


    path('tt_lesson/register/', views.tt_lesson_register, name='tt_lesson_register'),

    # path(r'group_semester/ajax/load_max_semester/?(?P<group_id>\d+)?/?$', views.load_max_semester, name='ajax_load_max_semester'),
    path('group_semester/ajax/load_max_semester', views.load_max_semester, name='ajax_load_max_semester')

]
