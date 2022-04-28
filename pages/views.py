from django.shortcuts import render

# Functions for home
def job_search(request):
    job_search_context = {}
    search_keyword_input = request.GET.get('search_keyword')
    search_location_input = request.GET.get('search_location')
    min_salary_input = request.GET.get('min_salary', '')
    max_salary_input = request.GET.get('max_salary', '')
    min_experience_input = request.GET.get('min_experience', '')
    max_experience_input = request.GET.get('max_experience', '')
    is_remote_input = request.GET.get('is_remote', '')
    job_type_input = request.GET.get('job_type', '')
    industry_input = request.GET.get('industry', '')
    created_date_input = request.GET.get('created_date', '')
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
            'created_date': created_date_input,
        },
    }
    # TODO: implement actual search logic
    job_search_context['job_search_result'] = [1, ]
    return job_search_context

# Create your views here.
def icons_test_view(request):
    context = {}
<<<<<<< HEAD
    if request.user.is_anonymous:
        # TODO: use models to count stats for counters
        context['counters'] = {
            'employer_count': 2892,
            'job_seeker_count': 371,
            'job_post_count': 356,
            'hired_count': 903,
        }
        if request.GET:
            context.update(job_search(request))
        return render(request, 'pages/home/visitor_home.html', context)
    elif request.user.role.role_name == 'JOB SEEKER':
        return render(request, 'pages/home/job_seeker_home.html', context)
    elif request.user.role.role_name == 'EMPLOYER':
        return render(request, 'pages/home/employer_home.html', context)
    elif request.user.role.role_name == 'INTERVIEWER':
        return render(request, 'pages/home/interviewer_home.html', context)
    else:
        return render(request, 'pages/home/visitor_home.html', context)
=======
    return render(request, 'pages/icons_test.html', context)
>>>>>>> parent of 62c95ff... fourth commit
