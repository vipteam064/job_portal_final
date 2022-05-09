from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from job_portal_final.custom_fields import *

# Create your models here.
class Role_master(models.Model):
    role_name = UpperCharField(
        max_length=20,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'^(?! )(?:[a-zA-Z]| (?! ))+(?<! )$',
                message="Role name must contain only letters and spaces."
            ),
        ],
        error_messages={
            'unique': _('A role with that name already exists.'),
        }
    )

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = 'Role'

class User_accountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set.')
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        admin_role = Role_master.objects.get(role_name='ADMIN') # make sure ADMIN role exists
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', admin_role)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') is not admin_role:
            raise ValueError('Superuser must belong to ADMIN role.')
        return self.create_user(email, password, **extra_fields)

class User_account(AbstractBaseUser, PermissionsMixin):
    email = UpperEmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email address already exists.'),
        },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into the admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    role = models.ForeignKey(
        Role_master,
        on_delete=models.PROTECT,
        help_text=_('Designates what role the user belongs to.'),
    )
    # related_employer = models.ForeignKey(
    #     'Employer_profile',
    #     blank=True,
    #     null=True,
    #     default=None,
    #     on_delete=models.CASCADE,
    #     help_text=_(
    #         'For relating user of interviewer role to an employer profile.')
    # )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = User_accountManager()

    def clean(self):
        error_dict = {}
        if hasattr(self, 'role'):
            # NOTE: checking based on predefined role_name
            # checking is_staff and is_superuser
            if self.role.role_name == 'ADMIN':
                if not self.is_staff:
                    error_dict['is_staff'] = 'User of admin role must have is_staff equal to true.'
                if not self.is_superuser:
                    error_dict['is_superuser'] = 'User of admin role must have is_superuser equal to true.'
            elif self.role.role_name == 'STAFF':
                if not self.is_staff:
                    error_dict['is_staff'] = 'User of staff role must have is_staff equal to true.'
                if self.is_superuser:
                    error_dict['is_superuser'] = 'Invalid permissions for user belonging to staff role.'
            else:
                if self.is_staff:
                    error_dict['is_staff'] = 'Invalid permissions for user.'
                if self.is_superuser:
                    error_dict['is_superuser'] = 'Invalid permissions for user.'

            # checking related_employer
            # if self.role.role_name == 'INTERVIEWER' and self.related_employer is None:
            #     error_dict['related_employer'] = 'Related employer must be provided for user belonging interviewer role.'
            # elif self.role.role_name != 'INTERVIEWER' and self.related_employer is not None:
            #     error_dict['related_employer'] = 'Related employer can only be set for user belonging interviewer role.'

        raise ValidationError(error_dict)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email.lower()
