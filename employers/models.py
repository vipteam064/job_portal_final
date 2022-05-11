from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE, PROTECT
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime
import decimal
from job_portal_final.custom_fields import *
import job_portal_final.myvalidators as myvalidators

# Create your models here.
class Employer_profile(models.Model):
    employer = models.OneToOneField(
        'users.User_account',
        limit_choices_to={'role__role_name': 'EMPLOYER'},
        on_delete=PROTECT,
        primary_key=True
    )
    company_name = UpperCharField(
        max_length=50,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'[a-zA-Zà-öÀ-Öø-þØ-Þ]+',
                message='Company name should contain atleast one letter.'
            ),
            validators.RegexValidator(
                regex=myvalidators.company_name_regex,
                message='Company name must contain only letters, digits, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).'
            ),
        ],
        error_messages={
            'unique': _('A company with that name already exists.'),
        }
    )
    company_description = models.TextField(max_length=500)
    establishment_date = models.DateField(validators=[
        validators.MaxValueValidator(datetime.date.today, message='Establishment date must be today or prior to today.'),
    ])
    industry = models.ForeignKey('pages.Industry_master', on_delete=PROTECT)
    gstin = UpperCharField(
        max_length=15,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[0-9]{2}[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}[1-9a-zA-Z]{1}[zZaAbBe-jE-J1-9][0-9a-zA-Z]{1}$',
                message='GSTIN is invalid.'
            ),
        ]
    )
    address = models.TextField(max_length=100)
    area = models.ForeignKey('pages.Area_master', on_delete=PROTECT)
    has_active_subscription = models.BooleanField(default=False)
    company_website = models.URLField()
    mobile_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'^\+91 [6-9]\d{9}$',
                message='Moblie number must be a valid Indian moblie number.'
            ),
        ],
        error_messages={
            'unique': _('An employer with that mobile number already exists.'),
        }
    )
    telephone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            validators.RegexValidator(
                regex=r'^\d{3} \d{7}|\d{4} \d{6}$',
                message='Telephone number must be in the format: \'999 9999999\' or \'9999 999999\'.'
            ),
        ]
    )
    contact_email = UpperEmailField(unique=True, error_messages={
        'unique': _('An employer with that contact email address already exists.'),
    })

    def __str__(self):
        return self.company_name

class Subscription(models.Model):
    employer_profile = models.ForeignKey(Employer_profile, on_delete=PROTECT)
    membership = models.ForeignKey('pages.Membership_master', on_delete=PROTECT)
    payment_time = models.DateTimeField(validators=[
        validators.MaxValueValidator(timezone.now, message='Payment time must be now or before now.'),
    ])
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(decimal.Decimal('0'), message='Amount must be greater than 0.'),
        ]
    )
    successful = models.BooleanField(default=False)
    end_date = models.DateField(blank=True, null=True)

class Job_post(models.Model):
    JOB_TYPE_CHOICES = ((False, 'Part-time'), (True, 'Full-time'))
    JOB_POST_STATUS_CHOICES = ((None, 'Draft'), (True, 'Active'), (False, 'Closed'))
    job_title = UpperCharField(
        max_length=40,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.job_title_regex,
                message='Job title must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).'
            ),
        ]
    )
    subscription = models.ForeignKey(Subscription, on_delete=PROTECT)
    job_description = models.TextField(max_length=500)
    job_type = models.BooleanField(choices=JOB_TYPE_CHOICES)
    job_industry = models.ForeignKey('pages.Industry_master', on_delete=PROTECT)
    address = models.TextField(max_length=100)
    city = models.ForeignKey('pages.City_master', on_delete=PROTECT)
    hrs_per_week = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            validators.MaxValueValidator(168, message='Hours per week must be less than or equal to 168.'),
        ]
    )
    is_remote = models.BooleanField(default=False)
    min_salary = models.PositiveIntegerField()
    max_salary = models.PositiveIntegerField()
    req_experience = models.PositiveSmallIntegerField()
    req_qualification = models.ManyToManyField('pages.Degree_master', blank=True, limit_choices_to=Q(degree_type__isnull=False), related_name='Job_post_req_qualification_set')
    min_edu = models.ForeignKey('pages.Degree_master', limit_choices_to={'degree_type': None}, related_name='Job_post_min_edu_set', on_delete=PROTECT)
    skill = models.ManyToManyField('pages.Skill_master')
    created_date = models.DateField(auto_now_add=True)
    activated_time = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        validators=[
            validators.MaxValueValidator(timezone.now, message='Activated time must be now or prior to now.'),
        ]
    )
    job_post_status = models.BooleanField(choices=JOB_POST_STATUS_CHOICES, blank=True, null=True, default=None)

    def clean(self):
        error_dict = {}
        if subscription.end_date < datetime.date.today():
            error_dict['__all__'] = 'Please subscribe to a membership to post a job.'

        if Job_post.objects.filter(subscription=self.subscription).count() >= subscription.membership.number_of_post:
            error_dict['__all__'] = 'You have reached the job post limit for currently subscribed membership.'

        if not (self.min_salary is None or self.max_salary is None):
            if self.min_salary > self.max_salary:
                error_dict['min_salary'] = 'Minimum salary must be less than or equal to maximum salary.'
                error_dict['max_salary'] = 'Maximum salary must be greater than or equal to minimum salary.'

        if self.id and self.req_qualification.filter(degree_type__isnull=True).exists():
            invalid_req_qualifications = self.req_qualification.filter(degree_type__isnull=True).values_list('degree_name')
            invalid_req_qualifications_str = ", ".join([str(i[0]) for i in invalid_req_qualifications])
            error_dict['req_qualification'] = f'Required qualifications must be degrees. {invalid_req_qualifications_str} {"is" if len(invalid_req_qualifications) == 1 else "are"} invalid.'

        if hasattr(self, 'min_edu') and self.min_edu.degree_type is not None:
            error_dict['min_edu'] = 'Minimum education must be an educational level.'

        try:
            old_job_post = Job_post.objects.get(id=self.id)
            if old_job_post.job_post_status != self.job_post_status:
                if not((old_job_post.job_post_status is None and self.job_post_status) or (old_job_post.job_post_status and self.job_post_status is False)):
                    error_dict['job_post_status'] = f'Job posts with status of {old_job_post.get_job_post_status_display()} can\'t be set to {self.get_job_post_status_display()}.'
        except Job_post.DoesNotExist:
            pass

        if not self.job_post_status and self.activated_time is not None:
            error_dict['activated_time'] = 'Activated date can only be set for active jobs.'

        raise ValidationError(error_dict)

    def save(self, *args, **kwargs):
        if self.job_post_status and self.activated_time is None:
            self.activated_time = datetime.date.today()
        super(Job_post, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.job_title)

class Application(models.Model):
    APPLICATION_STATUS_CHOICES = (('00', 'Pending'), ('01', 'Denied'), ('10', 'Accepted'), ('11', 'Hired'))
    job_post = models.ForeignKey(Job_post, on_delete=PROTECT)
    job_seeker_profile = models.ForeignKey('job_seekers.Job_seeker_profile', on_delete=PROTECT)
    employer_profile = models.ForeignKey(Employer_profile, on_delete=PROTECT)
    application_date = models.DateField(auto_now_add=True)
    application_status = models.BinaryField(max_length=2, default=b'00', choices=APPLICATION_STATUS_CHOICES)

    def clean(self):
        error_dict = {}
        try:
            old_application = Application.objects.get(id=self.id)
            if old_application.application_status != self.application_status:
                if not((old_application.application_status == '00' and self.application_status != '11') or (old_application.application_status == '10' and self.application_status == '11')):
                    error_dict['status'] = f'Application with status of {old_application.get_application_status_display()} can\'t be set to {self.get_application_status_display()}.'
        except Application.DoesNotExist:
            pass

        raise ValidationError(error_dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_application', fields=['job_post', 'job_seeker_profile', 'employer_profile']),
        ]
