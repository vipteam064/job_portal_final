from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth, messages
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import *

# Create your views here.
@user_passes_test(lambda user: not user.is_authenticated, login_url='/', redirect_field_name=None)
def signup_view(request):
    context = {}
    if request.method == 'POST':
        role_input = request.POST.get('role')
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        confirm_password_input = request.POST.get('confirm_password')
        context['form'] = {
            'role': role_input,
            'email': email_input,
        }
        if role_input == "JOB SEEKER" or role_input == "EMPLOYER":
            role = Role_master.objects.get(role_name = role_input)
            try:
                if password_input == confirm_password_input:
                    user_account = User_account(email=email_input, role=role)
                    try:
                        validate_password(password_input, user_account)
                    except ValidationError as e:
                        raise ValidationError({'password': e}) # converting error_list to error_dict with key 'password'
                    user_account.set_password(password_input)
                    user_account.full_clean()
                    user_account.save()
                    user_account = auth.authenticate(request, email=email_input, password=password_input)
                    auth.login(request, user_account)
                    user_account.email_user('Account Created!', 'You have been successfully registered to job portal.')
                    if user_account.role.role_name == 'JOB SEEKER':
                        return HttpResponse('personal details')
                    else:
                        return HttpResponse('employer details')
                else:
                    raise ValidationError({'confirm_password': 'Password and confirm password don\'t match.'})
            except ValidationError as e:
                if hasattr(e, 'error_dict'):
                    context['errors'] = e.message_dict.items()
                else:
                    context['errors'] = [('__all__', e), ]
        else:
            context['errors'] = [('role', ['Please select either job seeker or employer.'])]
    return render(request, 'users/signup.html', context)

def login_view(request):
    context = {}
    if request.method == 'POST':
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        user_account = auth.authenticate(request, email=email_input, password=password_input)
        if user_account is not None:
            auth.login(request, user_account)
            redirect_url = request.GET.get('next')
            if redirect_url:
                return redirect(redirect_url)
            else:
                if user_account.role.role_name == "ADMIN" or user_account.role.role_name == "STAFF":
                    return redirect('/admin/')
                else:
                    return HttpResponse('home')
        else:
            context['errors'] = [('__all__', ['Invalid email or password!']), ]
    return render(request, 'users/login.html', context)

def logout_view(request):
    auth.logout(request)
    return redirect('/')

@login_required
def change_email_view(request):
    context = {}
    if request.method == 'POST':
        try:
            email_input = request.POST.get('email').strip().lower()
            user_account = request.user
            curr_email = user_account.email.lower()
            if email_input != curr_email:
                user_account.email = email_input
                user_account.full_clean()
                User_account.objects.get(id=request.user.id).email_user('Email Changed!', 'Your registered email has been changed from {} to {}.'.format(curr_email, user_account.email.lower()))
                user_account.save()
                messages.success(request, 'Email changed successfully!')
                return HttpResponse('home')
            else:
                raise ValidationError({'email': 'New email can\'t be same as current email.'})
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                context['errors'] = e.message_dict.items()
            else:
                context['errors'] = [('__all__', e), ]
    return render(request, 'users/change_email.html', context)
