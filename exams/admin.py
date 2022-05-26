from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Exam_master)
admin.site.register(Question)
admin.site.register(Employer_exam_candidate)
admin.site.register(Employer_exam_ans)
admin.site.register(Practice_test_candidate)
admin.site.register(Practice_test_ans)
