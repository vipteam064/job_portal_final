from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.core import validators
from django.core.exceptions import ValidationError
from job_portal_final.custom_fields import *
import job_portal_final.myvalidators as myvalidators

# Create your models here.
class Interview_master(models.Model):
    interview_name = UpperCharField(
        max_length=40,
        validators=[
            validators.RegexValidator(
                regex=myvalidators.job_title_regex,
                message='Interview name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).'
            ),
        ]
    )
    interviewer = models.ManyToManyField('users.User_account', through='Interview_result')
    employer_profile = models.ForeignKey('employers.Employer_profile', on_delete=PROTECT)
    job_post = models.ForeignKey('employers.Job_post', on_delete=PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def clean(self):
        error_dict = {}
        if self.job_post.job_post_status is not False:
            error_dict['job_post'] = 'Please close the job post to be able to create interviews for it.'

        if self.interviewer and self.interviewer.exclude(related_employer=self.employer_profile).exists():
            invalid_interviewers = self.interviewer.exclude(related_employer=self.employer_profile)
            invalid_interviewers_str = ', '.join([str(i) for i in invalid_interviewers_str])
            error_dict['interviewer'] = f'You can only assign interviewer accounts created by you to the interview. {invalid_interviewers_str} {"is" if len(invalid_interviewers) == 1 else "are"} invalid.'

        raise ValidationError(error_dict)

    def __str__(self):
        return self.interview_name

    class Meta:
        verbose_name = 'Interview'

class Interview_result(models.Model):
    interview = models.ForeignKey(Interview_master, on_delete=CASCADE)
    interviewer = models.ForeignKey('users.User_account', on_delete=PROTECT)
    application = models.ForeignKey('employers.Application', on_delete=PROTECT)
    result = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            validators.MaxValueValidator(100, message='Result must be less than or equal to 100.')
        ]
    )
    date = models.DateField(blank=True, null=True, default=None)

    def clean(self):
        if self.application.application_status != 3:
            raise ValidationError({'application': f'Interview candidate must be an accepted applicant. {self.application.job_seeker_profile} has invalid application status - {self.application.get_application_status_display()}'})

    def save(self, *args, **kwargs):
        if self.result is not None:
            self.date = datetime.date.today()
        super(Interview_result, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.application.job_seeker_profile)

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_interview_result', fields=['interview', 'interviewer', 'application']),
        ]
