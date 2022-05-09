from django.db import models

# Create your models here.
# class Employer_profile(models.Model):
#     employer = models.OneToOneField(User_account, limit_choices_to={
#                                     'role__role_name': 'EMPLOYER'}, on_delete=PROTECT, primary_key=True)
#     company_name = UpperCharField(
#         max_length=50,
#         unique=True,
#         validators=[
#             validators.RegexValidator(
#                 regex=r'[a-zA-Zà-öÀ-Öø-þØ-Þ]+', message='Company name should contain atleast one letter.'),
#             validators.RegexValidator(regex=myvalidators.company_name_regex,
#                                       message='Company name must contain only letters, digits, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).')
#         ]
#     )
#     company_description = models.TextField(max_length=500)
#     establishment_date = models.DateField(validators=[
#         validators.MaxValueValidator(
#             datetime.date.today, message='Establishment date must be today or prior to today.')
#     ])
#     industry = models.ForeignKey(Industry_master, on_delete=PROTECT)
#     gstin = UpperCharField(
#         max_length=15,
#         unique=True,
#         validators=[
#             validators.RegexValidator(
#                 regex=r'^[0-9]{2}[a-zA-Z]{5}[0-9]{4}[a-zA-Z]{1}[1-9a-zA-Z]{1}[zZaAbBe-jE-J1-9][0-9a-zA-Z]{1}$', message='GSTIN is invalid.')
#         ]
#     )
#     address = models.TextField(max_length=100)
#     area = models.ForeignKey(Area_master, on_delete=PROTECT)
#     has_membership = models.BooleanField(default=False)
#     company_website = models.URLField()
#     mobile_number = models.CharField(
#         max_length=20,
#         unique=True,
#         validators=[
#             validators.RegexValidator(
#                 regex=r'^\+91 [6-9]\d{9}$', message='Moblie number must be a valid Indian moblie number.')
#         ],
#         error_messages={
#             'unique': _('An employer with that mobile number already exists.'),
#         }
#     )
#     telephone_number = models.CharField(
#         max_length=20,
#         blank=True,
#         validators=[
#             validators.RegexValidator(
#                 regex=r'^\d{3} \d{7}|\d{4} \d{6}$', message='Telephone number must be in the format: 3 to 4 digit STD code, space, 6 to 7 digit fixed-line number.')
#         ]
#     )
#     email = UpperEmailField(unique=True, error_messages={
#         'unique': _('An employer with that email address already exists.'),
#     })
#
#     def __str__(self):
#         return str(self.employer_id)
#
# class Subscription(models.Model):
#     # TODO: set subscription fields based on payment gateway
#     employer_profile = models.ForeignKey(Employer_profile, on_delete=PROTECT)
#     membership = models.ForeignKey(Membership_master, on_delete=PROTECT)
#     payment_time = models.DateTimeField(validators=[
#         validators.MaxValueValidator(
#             timezone.now, message='Payment time must be now or before now.')
#     ])
#     amount = models.DecimalField(
#         max_digits=7,
#         decimal_places=2,
#         validators=[
#             validators.MinValueValidator(decimal.Decimal(
#                 '0'), message='Amount must be greater than 0.')
#         ]
#     )
#     successful = models.BooleanField(default=False)
#     end_date = models.DateField(blank=True, null=True)
#
# class Job_post(models.Model):
#     JOB_TYPE_CHOICES = ((True, 'Full-time'), (False, 'Part-time'))
#     JOB_POST_STATUS_CHOICES = (
#         (None, 'Draft'), (True, 'Active'), (False, 'Closed'))
#     job_title = UpperCharField(
#         max_length=40,
#         validators=[
#             validators.RegexValidator(regex=myvalidators.job_title_regex,
#                                       message='Job title must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).')
#         ]
#     )
#     subscription = models.ForeignKey(
#         Subscription, limit_choices_to=myvalidators.active_subscription_limit_choices, on_delete=PROTECT)
#     job_description = models.TextField(max_length=500)
#     job_type = models.BooleanField(choices=JOB_TYPE_CHOICES)
#     job_industry = models.ForeignKey(Industry_master, on_delete=PROTECT)
#     address = models.TextField(max_length=100)
#     city = models.ForeignKey(City_master, on_delete=PROTECT)
#     hrs_per_week = models.PositiveSmallIntegerField(
#         blank=True,
#         null=True,
#         validators=[
#             validators.MaxValueValidator(
#                 168, message='Hours per week must be less than or equal to 168.')
#         ]
#     )
#     is_remote = models.BooleanField(default=False)
#     min_salary = models.PositiveIntegerField()
#     max_salary = models.PositiveIntegerField()
#     req_experience = models.PositiveSmallIntegerField()
#     req_qualification = models.ManyToManyField(Degree_master, blank=True, limit_choices_to=Q(
#         degree_type__isnull=False), related_name='Job_post_req_qualification_set')
#     min_edu = models.ForeignKey(Degree_master, limit_choices_to={
#                                 'degree_type': None}, related_name='Job_post_min_edu_set', on_delete=PROTECT)
#     skill = models.ManyToManyField(Skill_master)
#     created_date = models.DateField(auto_now_add=True)
#     activated_time = models.DateTimeField(
#         blank=True,
#         null=True,
#         default=None,
#         validators=[
#             validators.MaxValueValidator(
#                 timezone.now, message='Activated time must be now or prior to now.')
#         ]
#     )
#     job_post_status = models.BooleanField(
#         choices=JOB_POST_STATUS_CHOICES, blank=True, null=True, default=None)
#
#     def clean(self):
#         error_dict = {}
#         if self.min_salary is not None and self.max_salary is not None:
#             if self.min_salary > self.max_salary:
#                 error_dict['min_salary'] = 'Minimum salary must be less than or equal to maximum salary.'
#                 error_dict['max_salary'] = 'Maximum salary must be greater than or equal to minimum salary.'
#
#         if self.id and self.req_qualification.filter(degree_type__isnull=True).exists():
#             error_dict['req_qualification'] = 'Required qualifications must be degrees.'
#
#         if hasattr(self, 'min_edu') and self.min_edu.degree_type is not None:
#             error_dict['min_edu'] = 'Minimum education must be an educational level.'
#
#         try:
#             old_status = Job_post.objects.get(id=self.id).job_post_status
#             if old_status != self.job_post_status:
#                 if not((old_status is None and self.job_post_status) or (old_status and self.job_post_status is False)):
#                     old_status_text = [
#                         choice[1] for choice in self.JOB_POST_STATUS_CHOICES if choice[0] == old_status][0]
#                     error_dict['job_post_status'] = 'Job posts with status of %s can\'t be set to %s' % (
#                         old_status_text, self.get_job_post_status_display())
#         except Job_post.DoesNotExist:
#             pass
#
#         if not self.job_post_status and self.activated_time is not None:
#             error_dict['activated_time'] = 'Activated date can only be set for active jobs.'
#
#         raise ValidationError(error_dict)
#
#     def save(self, *args, **kwargs):
#         if self.job_post_status and self.activated_time is None:
#             self.activated_time = datetime.date.today()
#         super(Job_post, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return str(self.job_title)
#
# class Application(models.Model):
#     STATUS_CHOICES = ((None, 'Pending'), (True, 'Accepted'), (False, 'Denied'))
#     job_post = models.ForeignKey(Job_post, on_delete=PROTECT)
#     job_seeker_profile = models.ForeignKey(
#         Job_seeker_profile, on_delete=PROTECT)
#     employer_profile = models.ForeignKey(Employer_profile, on_delete=PROTECT)
#     application_date = models.DateField(auto_now_add=True)
#     status = models.BooleanField(
#         blank=True, null=True, default=None, choices=STATUS_CHOICES)
#     hired = models.BooleanField(blank=True, null=True, default=None)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(name='unique_application', fields=[
#                                     'job_post', 'job_seeker_profile', 'employer_profile']),
#         ]
#
#     def clean(self):
#         error_dict = {}
#         try:
#             old_status = Application.objects.get(id=self.id).status
#             if old_status != self.status and old_status is not None:
#                 old_status_text = [
#                     choice[1] for choice in self.STATUS_CHOICES if choice[0] == old_status][0]
#                 error_dict['status'] = 'Application with status of %s can\'t be set to %s' % (
#                     old_status_text, self.get_job_post_status_display())
#         except Application.DoesNotExist:
#             pass
#
#         if self.status is None and self.hired is not None:
#             error_dict['hired'] = 'Application with status pending cannot be set as hired.'
#
#         raise ValidationError(error_dict)
