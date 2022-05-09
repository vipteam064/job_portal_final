from django.db import models

# Create your models here.
# class Interview_master(models.Model):
#     interview_name = UpperCharField(
#         max_length=40,
#         validators=[
#             validators.RegexValidator(
#                 regex=myvalidators.job_title_regex, message='Interview name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).')
#         ]
#     )
#     interviewer = models.ManyToManyField(User_account, limit_choices_to={
#                                          'role__role_name': 'INTERVIEWER'})
#     employer_profile = models.ForeignKey(Employer_profile, on_delete=PROTECT)
#     job_post = models.ForeignKey(Job_post, limit_choices_to=Q(
#         job_post_status__isnull=False), on_delete=PROTECT)
#     start_date = models.DateField()
#     end_date = models.DateField(blank=True, null=True)
#
#     def __str__(self):
#         return self.interview_name
#
# class Interview_result(models.Model):
#     interview = models.ForeignKey(Interview_master, on_delete=PROTECT)
#     application = models.ForeignKey(Application, limit_choices_to={
#                                     'status': True}, on_delete=PROTECT)
#     interviewer = models.ForeignKey(User_account, limit_choices_to={
#                                     'role__role_name': 'INTERVIEWER'}, on_delete=PROTECT)
#     result = models.PositiveSmallIntegerField(
#         blank=True,
#         null=True,
#         validators=[
#             validators.MaxValueValidator(
#                 100, message='Result must be less than or equal to 100.')
#         ]
#     )
#     date = models.DateField(blank=True, null=True, default=None)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(name='unique_interview_result', fields=[
#                                     'interview', 'application', 'interviewer']),
#         ]
#
#     def save(self, *args, **kwargs):
#         if self.result is not None:
#             self.date = datetime.date.today()
#         super(Interview_result, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return str(self.application)
