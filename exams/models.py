from django.db import models

# Create your models here.
# class Exam_master(models.Model):
#     EXAM_TYPE_CHOICES = ((True, 'Employer exam'), (False, 'Practice test'))
#     exam_name = UpperCharField(
#         max_length=40,
#         validators=[
#             validators.RegexValidator(
#                 regex=myvalidators.job_title_regex, message='Exam name must contain only letters, spaces, \' (apostrophes), () (parenthesis), - (hyphens), , (commas) and . (full-stops).')
#         ]
#     )
#     exam_type = models.BooleanField(choices=EXAM_TYPE_CHOICES)
#     job_post = models.ForeignKey(Job_post, blank=True, null=True, limit_choices_to=Q(
#         job_post_status__isnull=False), on_delete=PROTECT)
#     employer_profile = models.ForeignKey(
#         Employer_profile, blank=True, null=True, on_delete=PROTECT)
#     start_time = models.DateTimeField(blank=True, null=True)
#     duration = models.PositiveSmallIntegerField(
#         validators=[
#             validators.MinValueValidator(
#                 5, message='Duration must be greater than or equal to 5 minutes.')
#         ]
#     )
#
#     def clean(self):
#         # TODO: add validations based on exam_type
#         pass
#
#     def __str__(self):
#         return self.exam_name
#
#     class Meta:
#         verbose_name = 'Exam'
#
# class Question(models.Model):
#     exam_master = models.ForeignKey(Exam_master, on_delete=PROTECT)
#     question_stem = models.TextField()
#     correct_ans = models.PositiveSmallIntegerField(validators=[
#         validators.MinValueValidator(
#             1, 'Correct answer must be a valid choice.'),
#         validators.MaxValueValidator(
#             4, 'Correct answer must be a valid choice.')
#     ])
#     choice1 = models.CharField(max_length=70)
#     choice2 = models.CharField(max_length=70)
#     choice3 = models.CharField(max_length=70)
#     choice4 = models.CharField(max_length=70)
#
# class Employer_exam_candidate(models.Model):
#     exam_master = models.ForeignKey(Exam_master, limit_choices_to={
#                                     'exam_type': True}, on_delete=PROTECT)
#     application = models.ForeignKey(Application, limit_choices_to={
#                                     'status': True}, on_delete=PROTECT)
#     obtained_marks = models.PositiveSmallIntegerField(blank=True, null=True)
#     attempted = models.BooleanField(default=False)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(name='unique_exam_candidate', fields=[
#                                     'exam_master', 'application']),
#         ]
#
# class Employer_exam_ans(models.Model):
#     exam_master = models.ForeignKey(Exam_master, on_delete=PROTECT)
#     application = models.ForeignKey(Application, on_delete=PROTECT)
#     question = models.ForeignKey(Question, on_delete=PROTECT)
#     submitted_ans = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
#         validators.MinValueValidator(
#             1, 'Submitted answer must be a valid choice.'),
#         validators.MaxValueValidator(
#             4, 'Submitted answer must be a valid choice.')
#     ])
#
#     class Meta:
#         unique_together = (
#             ('exam_master_id', 'application_id', 'question_id'),)
#
# class Practice_test_candidate(models.Model):
#     exam_master = models.ForeignKey(Exam_master, limit_choices_to={
#                                     'exam_type': False}, on_delete=PROTECT)
#     job_seeker_profile = models.ForeignKey(
#         Job_seeker_profile, on_delete=PROTECT)
#     obtained_marks = models.PositiveSmallIntegerField()
#
#     class Meta:
#         unique_together = (('exam_master', 'job_seeker_profile'),)
#
# class Practice_test_ans(models.Model):
#     exam_master = models.ForeignKey(Exam_master, on_delete=PROTECT)
#     job_seeker_profile = models.ForeignKey(
#         Job_seeker_profile, on_delete=PROTECT)
#     question = models.ForeignKey(Question, on_delete=PROTECT)
#     submitted_ans = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
#         validators.MinValueValidator(
#             1, 'Submitted answer must be a valid choice.'),
#         validators.MaxValueValidator(
#             4, 'Submitted answer must be a valid choice.')
#     ])
#
#     class Meta:
#         unique_together = (('exam_master', 'job_seeker_profile', 'question'))
