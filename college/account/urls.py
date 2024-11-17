"""
URL configuration for account app.
"""
from django.urls import path, register_converter, re_path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .converters import DateConverter
from .forms import CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm
from .views import home

app_name = 'account'

register_converter(DateConverter, 'date')

urlpatterns = [
    re_path(r'^home/$', views.home, name='home'),
    # path('', include('django.contrib.auth.urls')),
    re_path(r'^login/$', auth_views.LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^password_change/$', auth_views.PasswordChangeView.as_view(form_class=CustomPasswordChangeForm, success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    re_path(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm, success_url=reverse_lazy('account:password_reset_done')), name='password_reset'),
    re_path(r'^password_reset/done$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm, success_url=reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # re_path(r'^password_reset/$', auth_views.),

# account/ login/ [name='login']
# account/ logout/ [name='logout']
# account/ password_change/ [name='password_change']
# account/ password_change/done/ [name='password_change_done']
# account/ password_reset/ [name='password_reset']
# account/ password_reset/done/ [name='password_reset_done']
# account/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# account/ reset/done/ [name='password_reset_complete']

    # path('loginn/', auth_views.LoginView.as_view(), name='login'),
    # path('loginn/', views.user_login, name='login'),

    path('', views.welcome, name='welcome'),

    path('user/', views.user_list, name='user_list'),
    path('user/details/<int:id>', views.user_details, name='user_details'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/edit/<int:id>', views.user_edit, name='user_edit'),
    path('user/delete/<int:id>', views.user_delete, name='user_delete'),
    path('user/delete/<int:id>/tutor', views.user_delete_tutor, name='user_delete_tutor'),
    path('user/delete/<int:id>/student', views.user_delete_student, name='user_delete_student'),

    # path('lgout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='user_logout'),







    # path(r'group_semester/ajax/load_max_semester/?(?P<group_id>\d+)?/?$', views.load_max_semester, name='ajax_load_max_semester'),


]
