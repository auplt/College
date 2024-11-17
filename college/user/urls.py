"""
URL configuration for user app.
"""

from django.urls import path, register_converter, re_path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from timetable.converters import DateConverter
from .forms import CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm

app_name = 'user'

register_converter(DateConverter, 'date')

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    re_path(r'^home/$', views.home, name='home'),
    re_path(r'^login/$', auth_views.LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^password_change/$',
            auth_views.PasswordChangeView.as_view(form_class=CustomPasswordChangeForm,
                                                  success_url=reverse_lazy('user:password_change_done')),
            name='password_change'),
    re_path(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    re_path(r'^password_reset/$',
            auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm,
                                                 success_url=reverse_lazy('user:password_reset_done')),
            name='password_reset'),
    re_path(r'^password_reset/done$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',
         auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm,
                                                     success_url=reverse_lazy('user:password_reset_complete')),
         name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('list/', views.user_list, name='user_list'),
    path('details/<int:id>', views.user_details, name='user_details'),
    path('register/', views.user_register, name='user_register'),
    path('edit/<int:id>', views.user_edit, name='user_edit'),
    path('delete/<int:id>', views.user_delete, name='user_delete'),
    path('delete/<int:id>/tutor', views.user_delete_tutor, name='user_delete_tutor'),
    path('delete/<int:id>/student', views.user_delete_student, name='user_delete_student'),
]
