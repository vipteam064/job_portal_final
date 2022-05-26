from django.shortcuts import render
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from .models import *
from users.models import *
from job_seekers.models import *
from employers.models import *

# Functions for home
def job_search(request):
    # print(request.GET)
    job_search_context = {}
    search_keyword_input = request.GET.get('search_keyword').strip()
    search_location_input = request.GET.get('search_location').strip()
    min_salary_input = request.GET.get('min_salary', '').strip()
    max_salary_input = request.GET.get('max_salary', '').strip()
    min_experience_input = request.GET.get('min_experience', '').strip()
    max_experience_input = request.GET.get('max_experience', '').strip()
    is_remote_input = request.GET.get('is_remote', '').strip()
    job_type_input = request.GET.get('job_type', '').strip()
    industry_input = request.GET.get('industry', '').strip()
    activated_time_input = request.GET.get('activated_time', '').strip()
    job_search_context['form'] = {
        'search_keyword': search_keyword_input,
        'search_location': search_location_input,
        'search_filters': {
            'min_salary': min_salary_input,
            'max_salary': max_salary_input,
            'min_experience': min_experience_input,
            'max_experience': max_experience_input,
            'is_remote': is_remote_input,
            'job_type': job_type_input,
            'industry': industry_input,
            'activated_time': activated_time_input,
        },
    }
    job_search_context['industries'] = Industry_master.objects.all()

    job_search_results = Job_post.objects.filter(job_post_status=True)
    search_keyword_query = Q(skill__skill_name=search_keyword_input) | Q(job_title__icontains=search_keyword_input)
    search_location_query = Q(city__state__state_name=search_location_input) | Q(city__city_name=search_location_input)
    if search_keyword_input and search_location_input:
        job_search_results = job_search_results.filter(search_keyword_query, search_location_query)
    elif search_keyword_input:
        job_search_results = job_search_results.filter(search_keyword_query)
    elif search_location_input:
        job_search_results = job_search_results.filter(search_location_query)

    if len(request.GET) > 2 and job_search_results.exists():
        if min_salary_input and max_salary_input:
            if int(min_salary_input) <= int(max_salary_input):
                job_search_results = job_search_results.filter(min_salary__gte=min_salary_input, max_salary__lte=max_salary_input)
            else:
                job_search_context['form']['search_filters']['min_salary'] = ''
                job_search_context['form']['search_filters']['max_salary'] = ''
                messages.warning(request, 'Minimum salary should be less than or equal to maximum salary.')
        elif min_salary_input:
            job_search_results = job_search_results.filter(min_salary__gte=min_salary_input)
        elif max_salary_input:
            job_search_results = job_search_results.filter(max_salary__lte=max_salary_input)

        if min_experience_input and max_experience_input:
            if int(min_experience_input) <= int(max_experience_input):
                job_search_results = job_search_results.filter(req_experience__gte=min_experience_input, req_experience__lte=max_experience_input)
            else:
                job_search_context['form']['search_filters']['min_experience'] = ''
                job_search_context['form']['search_filters']['max_experience'] = ''
                messages.warning(request, 'Minimum experience should be less than or equal to maximum experience.')
        elif min_experience_input:
                job_search_results = job_search_results.filter(req_experience__gte=min_experience_input)
        elif max_experience_input:
                job_search_results = job_search_results.filter(req_experience__lte=max_experience_input)

        if is_remote_input:
            job_search_results = job_search_results.filter(is_remote=int(is_remote_input))

        if job_type_input:
            job_search_results = job_search_results.filter(job_type=int(job_type_input))

        if industry_input:
            job_search_results = job_search_results.filter(job_industry_id=industry_input)

        if activated_time_input:
            job_search_results = job_search_results.filter(activated_time__gte=timezone.now()-relativedelta(days=int(activated_time_input)))

    job_search_context['job_search_results'] = job_search_results.distinct().order_by('-activated_time')
    return job_search_context

# Create your views here.
def home_view(request):
    context = {
        'counters': {
            'employer_count': Employer_profile.objects.count(),
            'job_seeker_count': Job_seeker_profile.objects.count(),
            'job_post_count': Job_post.objects.filter(job_post_status=True).count(),
            'hired_count': Application.objects.filter(application_status=4).count(),
        },
    }
    if request.user.is_anonymous:
        if request.GET:
            context.update(job_search(request))
        return render(request, 'pages/home/visitor_home.html', context)
    elif request.user.role.role_name == 'JOB SEEKER':
        if request.GET:
            context.update(job_search(request))
        return render(request, 'pages/home/job_seeker_home.html', context)
    elif request.user.role.role_name == 'EMPLOYER':
        context['counters'] = {
            'job_post_count': Job_post.objects.filter(subscription__employer_profile=request.user.employer_profile).count(),
            'active_post_count': Job_post.objects.filter(job_post_status=True).count(),
            'inactive_post_count': Job_post.objects.filter(job_post_status=False).count(),
        }
        return render(request, 'pages/home/employer_home.html', context)
    elif request.user.role.role_name == 'INTERVIEWER':
        # context['assigned_interviews'] = [{
        #     'job_post': {'job_title': 'test job',},
        #     'interview_name': 'test interview',
        #     'start_date': 3,
        #     'end_date': None,
        #     'related_interview_result': {'count': 5},
        # },]
        context['curr_date'] = 4
        return render(request, 'pages/home/interviewer_home.html', context)
    else:
        if request.GET:
            context.update(job_search(request))
        return render(request, 'pages/home/visitor_home.html', context)
