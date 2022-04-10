from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext, gettext_lazy as _

class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'pattern': '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', 'title': 'Password must be 8-20 characters long, contain lowercase and uppercase letters, numbers and special characters (@$!%*?&), and must not contain spaces or other characters'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Retype your new password', 'oninput': 'check_password(this)'}),
    )

class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'username@domain.com', 'pattern': '^[\w\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\.\-]+$', 'title': 'username@domain.com'})
    )

class CustomSetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'pattern': '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', 'title': 'Password must be 8-20 characters long, contain lowercase and uppercase letters, numbers and special characters (@$!%*?&), and must not contain spaces or other characters'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Retype your new password', 'oninput': 'check_password(this)'}),
    )
