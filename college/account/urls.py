"""
URL configuration for account app.
"""
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginView.as_view(), name='login'),


    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    # path('lgout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='user_logout'),
    path('register_group', views.register_group, name='register_group'),
    path('discipline/register', views.register_discipline, name='register_discipline'),
    path('classroom/register', views.register_classroom, name='register_classroom'),
    path('lesson_time/register', views.register_lesson_time, name='register_lesson_time'),
    path('group_semester/register', views.register_group_semester, name='register_group_semester'),
    path('group_member/register', views.register_group_member, name='register_group_member'),
    path('curriculum/register/', views.register_curriculum, name='register_curriculum'),
    path('curriculum_lesson/register/', views.register_curriculum_lesson, name='curriculum_lesson'),
    path('tt_lesson/register/', views.register_tt_lesson, name='tt_lesson'),

    path('group_semester/ajax/load_max_semester', views.load_max_semester, name='ajax_load_max_semester')

               ]
