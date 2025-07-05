from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Send email with user details
            subject = 'Welcome to SkillGrid!'
            message = f"""
            Thank you for signing up, {user.first_name}!

            Your details:
            Username: {user.username}
            Email: {user.email}
            First Name: {user.first_name}
            Last Name: {user.last_name}
            """
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            login(request, user)
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('core:home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:home')
