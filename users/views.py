from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import *

# Create your views here.
def signup_view(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        pwd1 = request.POST.get('pwd1')
        role = Role_master.objects.get(role_name=request.POST.get('role'))

        try:
            if pwd == pwd1:
                user = User_account(email=email, role=role)
                user.set_password(pwd)
                user.full_clean()
                user.save()
                user = authenticate(request, email=email, password=pwd)
                if user is not None:
                    login(request, user)
                    user.email_user('Account Created!', 'You have been successfully registered to job portal.')
                else:
                    return redirect('/users/login')
                if user.role.role_name == 'JOB SEEKER':
                    pass
                    # return redirect('personal details')
                elif user.role.role_name == 'EMPLOYER':
                    pass
                    # return redirect('employer details')
                elif user.role.role_name == 'INTERVIEWER':
                    pass
                    # return redirect('interviewer home')
                else:
                    pass
                    # return redirect('home')
                return HttpResponse('home')
            else:
                raise ValidationError({'password': 'Password and confirm password don\'t match.'})
        except ValidationError as e:
            context['errors'] = e.message_dict.items()

    return render(request, 'users/signup.html', context)

def login_view(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.role.role_name == "JOB SEEKER":
                pass
                # return redirect('jobseekerhome')
            elif user.role.role_name == "EMPLOYER":
                pass
                # return redirect('employerhome')
            elif user.role.role_name == "INTERVIEWER":
                pass
                # return redirect('interviewerhome')
            elif user.role.role_name == "ADMIN" or user.role.role_name == "STAFF":
                pass
                # return redirect('admin:index')
            else:
                pass
                # return redirect('home')
            return HttpResponse('home')
        else:
            context['errors'] = [('__all__', ['Invalid email or password!']), ]
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('/users/login')

def change_email_view(request):
    context = {}
    print(request.POST)
    print(request.user)
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user = User_account.objects.get(id=request.user.id)
            old_email = user.email
            user.email = email
            user.full_clean()
            User_account.objects.get(id=request.user.id).email_user('Email Changed!', 'Your registered email has been changed from {} to {}.'.format(old_email.lower(), user.email.lower()))
            user.save()
            if user.role.role_name == "JOB SEEKER":
                pass
                # return redirect('jobseekerhome')
            elif user.role.role_name == "EMPLOYER":
                pass
                # return redirect('employerhome')
            elif user.role.role_name == "INTERVIEWER":
                pass
                # return redirect('interviewerhome')
            elif user.role.role_name == "ADMIN" or user.role.role_name == "STAFF":
                pass
                # return redirect('admin:index')
            else:
                pass
                # return redirect('home')
            return HttpResponse('home')
        except ValidationError as e:
            context['errors'] = e.message_dict.items()
    return render(request, 'users/change_email.html', context)
