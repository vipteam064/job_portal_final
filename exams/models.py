from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE, PROTECT
from django.core import validators
from django.core.exceptions import ValidationError
from job_portal_final.custom_fields import *
import job_portal_final.myvalidators as myvalidators

# Create your models here.
class Exam_master(models.Model):
    EXAM_TYPE_CHOICES = ((True, 'Employer exam'), (False, 'Practice test'))
    exam_name = UpperCharField(
        max_length=40,
        validators=[
            validators.RegexValidator(
                regex=r'[a-zA-Zà-öÀ-Öø-þØ-Þ]+',
                message='Exam name should contain atleast one letter.'
            ),
            validators.RegexValidator(
                regex=myvalidators.company_name_regex,
                message='Exam name must contain only letters, digits, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).'
            ),
        ]
    )
    exam_type = models.BooleanField(choices=EXAM_TYPE_CHOICES)
    job_post = models.ForeignKey('employers.Job_post', blank=True, null=True, limit_choices_to=Q(job_post_status__isnull=False), on_delete=PROTECT)
    employer_profile = models.ForeignKey('employers.Employer_profile', blank=True, null=True, on_delete=PROTECT)
    start_time = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(5, message='Duration must be greater than or equal to 5 minutes.')
        ]
    )

    def clean(self):
        error_dict = {}
        if self.exam_type:
            if self.job_post is None:
                error_dict['job_post'] = 'Employer exam must be assigned to a job post.'
            elif self.job_post.job_post_status is not False:
                error_dict['job_post'] = 'Please close the job post to be able to create exams for it.'
            if self.employer_profile is None:
                error_dict['employer_profile'] = 'Employer exam must be created by an employer.'
            if self.start_time is None:
                error_dict['start_time'] = 'Employer exam must have a start time.'
            if self.job_post and self.employer_profile and (self.job_post.subscription.employer_profile != self.employer_profile):
                error_dict['job_post'] = 'Assigned job post is not created by this employer.'
        else:
            if self.job_post or self.employer_profile or self.start_time:
                error_dict['__all__'] = 'Practice test cannot be assigned a job post, employer or start time.'
        raise ValidationError(error_dict)

    def __str__(self):
        return self.exam_name

    class Meta:
        verbose_name = 'Exam'

class Question(models.Model):
    exam_master = models.ForeignKey(Exam_master, on_delete=CASCADE)
    question_stem = models.TextField()
    correct_ans = models.PositiveSmallIntegerField(validators=[
        validators.MinValueValidator(1, 'Correct answer must be a valid choice.'),
        validators.MaxValueValidator(4, 'Correct answer must be a valid choice.')
    ])
    choice1 = models.CharField(max_length=70)
    choice2 = models.CharField(max_length=70)
    choice3 = models.CharField(max_length=70)
    choice4 = models.CharField(max_length=70)

    def __str__(self):
        return self.question_stem

class Employer_exam_candidate(models.Model):
    exam_master = models.ForeignKey(Exam_master, limit_choices_to={'exam_type': True}, on_delete=PROTECT)
    application = models.ForeignKey('employers.Application', limit_choices_to={'status': 3}, on_delete=PROTECT)
    obtained_marks = models.PositiveSmallIntegerField(blank=True, null=True)
    attempted = models.BooleanField(default=False)

    def clean(self):
        if self.exam_master.exam_type is False:
            raise ValidationError({'exam_master': 'Employer exam candidate can only be added for employer exams.'})
        if self.application.status != 3:
            raise ValidationError({'application': f'Employer exam candidate must be an accepted applicant. {self.application.job_seeker_profile} has invalid application status - {self.application.get_application_status_display()}'})
        if obtained_marks is not None:
            total_marks = Question.objects.filter(exam_master=self.exam_master).count()
            if obtained_marks > total_marks:
                raise ValidationError({'obtained_marks': f'Obtained marks ({self.obtained_marks}) must be less than or equal to total marks ({total_marks}).'})

    def __str__(self):
        return str(self.application.job_seeker_profile)

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_exam_candidate', fields=['exam_master', 'application']),
        ]

class Employer_exam_ans(models.Model):
    exam_candidate = models.ForeignKey(Employer_exam_candidate, on_delete=PROTECT)
    question = models.ForeignKey(Question, on_delete=PROTECT)
    submitted_ans = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
        validators.MinValueValidator(1, 'Submitted answer must be a valid choice.'),
        validators.MaxValueValidator(4, 'Submitted answer must be a valid choice.')
    ])

    def clean(self):
        if self.question.exam_master != self.exam_candidate.exam_master:
            raise ValidationError({'question': f'Answered question ({self.question.question_stem[:25]}...) does not belong to this exam ({self.exam_candidate.exam_master.exam_name}).'})

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_exam_ans', fields=['exam_candidate', 'question']),
        ]

class Practice_test_candidate(models.Model):
    exam_master = models.ForeignKey(Exam_master, limit_choices_to={'exam_type': False}, on_delete=PROTECT)
    job_seeker_profile = models.ForeignKey('job_seekers.Job_seeker_profile', on_delete=PROTECT)
    obtained_marks = models.PositiveSmallIntegerField()

    def clean(self):
        if self.exam_master.exam_type is True:
            raise ValidationError({'exam_master': 'Practice test candidate can only be added for practice tests.'})
        total_marks = Question.objects.filter(exam_master=self.exam_master).count()
        if obtained_marks > total_marks:
            raise ValidationError({'obtained_marks': f'Obtained marks ({self.obtained_marks}) must be less than or equal to total marks ({total_marks}).'})

    def __str__(self):
        return str(self.job_seeker_profile)

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_test_candidate', fields=['exam_master', 'job_seeker_profile']),
        ]

class Practice_test_ans(models.Model):
    test_candidate = models.ForeignKey(Practice_test_candidate, on_delete=PROTECT)
    question = models.ForeignKey(Question, on_delete=PROTECT)
    submitted_ans = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
        validators.MinValueValidator(1, 'Submitted answer must be a valid choice.'),
        validators.MaxValueValidator(4, 'Submitted answer must be a valid choice.')
    ])

    def clean(self):
        if self.question.exam_master != self.test_candidate.exam_master:
            question_part = self.question.question_stem[:25] + '...' if len(self.question.question_stem) > 25 else ''
            raise ValidationError({'question': f'Answered question ({question_part}) does not belong to this test ({self.test_candidate.exam_master.exam_name}).'})

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_test_ans', fields=['test_candidate', 'question']),
        ]
