from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import *
from .views import *

app_name = 'users'
urlpatterns = [
    path('signup', signup_view, name='signup'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('change-email', change_email_view, name='change_email'),
    path('change-password', auth_views.PasswordChangeView.as_view(
        template_name='users/change_password.html',
        success_url='change-password/done',
        form_class=CustomPasswordChangeForm,
    ), name='change_password'),
    path('change-password/done', auth_views.PasswordChangeDoneView.as_view(template_name='users/change_password_done.html'), name='change_password_done'),
    path('reset-password', auth_views.PasswordResetView.as_view(
        template_name='users/reset_password.html',
        email_template_name='users/reset_password_email.html',
        success_url='reset-password/done',
        form_class=CustomPasswordResetForm,
    ), name='reset_password'),
    path('reset-password/done', auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password_done.html'), name='reset_password_done'),
    path('reset-password-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/reset_password_confirm.html',
        success_url='/users/reset-password-complete',
        form_class=CustomSetPasswordForm,
    ), name='reset_password_confirm'),
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password_complete.html'), name='reset_password_complete'),
]
