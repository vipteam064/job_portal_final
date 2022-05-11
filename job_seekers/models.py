from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE, PROTECT
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from job_portal_final.custom_fields import *
import job_portal_final.myvalidators as myvalidators

# Create your models here.
class Job_seeker_profile(models.Model):
    GENDER_CHOICES = ((False, 'Female'), (True, 'Male'))
    job_seeker = models.OneToOneField(
        'users.User_account',
        limit_choices_to={'role__role_name': 'JOB SEEKER'},
        on_delete=PROTECT,
        primary_key=True
    )
    first_name = UpperCharField(
        max_length=30,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.person_name_regex,
                message='First name must contain only letters, spaces, \' (apostrophes), - (hyphens), , (commas) and . (full-stops).'
            ),
        ]
    )
    last_name = UpperCharField(
        max_length=30,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.person_name_regex,
                message='Last name must contain only letters, spaces, \' (apostrophes), - (hyphens), , (commas) and . (full-stops).'
            ),
        ]
    )
    gender = models.BooleanField(choices=GENDER_CHOICES)
    dob = models.DateField(validators=[
        validators.MaxValueValidator(myvalidators.dob_limit_value, message='Job seeker must be 15 or older.'),
    ])
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
            'unique': _('A job seeker with that mobile number already exists.'),
        }
    )
    address = models.TextField(max_length=100)
    area = models.ForeignKey('pages.Area_master', on_delete=PROTECT)
    resume = models.FileField(
        upload_to='resume',
        blank=True,
        null=True,
        validators=[
            validators.FileExtensionValidator(['pdf'], message='Resume must be a pdf document.'),
        ]
    )
    profile_pic = models.ImageField(
        upload_to='profile_pic',
        blank=True,
        null=True,
    )
    skill = models.ManyToManyField('pages.Skill_master')

    def __str__(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()

class Educational_detail(models.Model):
    job_seeker_profile = models.ForeignKey(Job_seeker_profile, on_delete=CASCADE)
    degree = models.ForeignKey(
        'pages.Degree_master',
        limit_choices_to=Q(degree_type__isnull=False) | Q(degree_name='10TH CLASS') | Q(degree_name='12TH CLASS'),
        on_delete=PROTECT
    )
    institute = models.ForeignKey('pages.Institute_master', on_delete=PROTECT)
    passing_year = models.PositiveSmallIntegerField(validators=[
        validators.RegexValidator(regex=r'\d{4}', message='Passing year must be in YYYY format.'),
        validators.MaxValueValidator(myvalidators.passing_year_limit_value, message='Passing year must be current year or earlier.'),
    ])
    percentage = models.FloatField(validators=[
        validators.MinValueValidator(0, message='Percentage must be greater than or equal to 0.'),
        validators.MaxValueValidator(100, message='Percentage must be less than or equal to 100.'),
    ])
    specialization = models.CharField(
        max_length=30,
        blank=True,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.name_regex,
                message='Specialization must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens) and . (full-stops).'
            ),
        ]
    )

    def clean(self):
        error_dict = {}
        if hasattr(self, 'degree'):
            if hasattr(self, 'institute'):
                # To check if institute_type matches degree_type
                if self.degree.degree_type is None and self.institute.institute_type:
                    error_dict['institute'] = 'Institute must be a school for school level of education.'
                elif self.degree.degree_type is not None and self.institute.institute_type is False:
                    error_dict['institute'] = 'Institute must be a university or college for degree.'

            if hasattr(self, 'job_seeker_profile'):
                # NOTE: checking based on predefined degree_name
                # To check if '10TH CLASS' is done before '12TH CLASS'
                if self.degree.degree_name == '12TH CLASS':
                    tenth_educational_details = Educational_detail.objects.filter(job_seeker_profile=self.job_seeker_profile, degree__degree_name='10TH CLASS')
                    if not tenth_educational_details.exists():
                        error_dict['degree'] = 'Educational details of 10th class must be provided before entering details of 12th class.'
                    elif not (self.passing_year > tenth_educational_details.order_by('passing_year').last().passing_year):
                        error_dict['passing_year'] = 'Passing year of 12th class must be after passing year of 10th class (%s).' % tenth_educational_details.order_by('passing_year').last().passing_year
                # To check if 'BACHELOR' is before 'MASTER'
                elif self.degree.degree_type is not None and self.degree.degree_type.degree_name == 'MASTER':
                    bachelor_educational_details = self.__class__.objects.filter(job_seeker_profile=self.job_seeker_profile, degree__degree_type__degree_name='BACHELOR')
                    if not bachelor_educational_details.exists():
                        error_dict['degree'] = 'Educational details of Bachelor degree must be provided before entering details of Master degree.'
                    elif not (self.passing_year > bachelor_educational_details.order_by('passing_year').first().passing_year):
                        error_dict['passing_year'] = 'Passing year of Master degree must be after passing year of atleast one Bachelor (%s) degree.' % bachelor_educational_details.order_by('passing_year').first().passing_year

        raise ValidationError(error_dict)

    def __str__(self):
        if self.degree.degree_type:
            return f'{self.degree.degree_type.degree_name} OF {self.degree.degree_name} FROM {self.institute.institute_name}'
        else:
            return self.degree.degree_name

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_educational_detail', fields=['job_seeker_profile', 'degree']),
        ]

class Experience_detail(models.Model):
    EMPLOYMENT_TYPE_CHOICES = ((False, 'Part-time'), (True, 'Full-time'))
    job_seeker_profile = models.ForeignKey(Job_seeker_profile, on_delete=CASCADE)
    company_name = UpperCharField(
        max_length=50,
        validators=[
            validators.RegexValidator(
                regex=r'[a-zA-Zà-öÀ-Öø-þØ-Þ]+',
                message='Company name should contain atleast one letter.'
            ),
            validators.RegexValidator(
                regex=myvalidators.company_name_regex,
                message='Company name must contain only letters, digits, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).'
            ),
        ]
    )
    job_title = UpperCharField(
        max_length=40,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.job_title_regex,
                message='Job title must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).'
            ),
        ]
    )
    employment_type = models.BooleanField(choices=EMPLOYMENT_TYPE_CHOICES)
    start_date = models.DateField(validators=[
        validators.MaxValueValidator(datetime.date.today, message='Start date must be today or prior to today.')
    ])
    end_date = models.DateField(
        blank=True,
        null=True,
        validators=[
            validators.MaxValueValidator(datetime.date.today, message='End date must be today or prior to today.')
        ]
    )
    is_ongoing = models.BooleanField()

    def clean(self):
        if self.is_ongoing and self.end_date is not None:
            raise ValidationError({'is_ongoing': 'Ongoing jobs can\'t have an end date.'})
        elif not self.is_ongoing:
            if self.end_date is None:
                raise ValidationError({'is_ongoing': 'Jobs which are not ongoing must have an end date.'})
            elif self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must not be proir to start date.'})

    def __str__(self):
        return self.job_title + ' AT ' + self.company_name
