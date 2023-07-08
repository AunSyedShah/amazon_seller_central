from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.
def register_user(request):
    context = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('account_app:login')
        else:
            messages.error(request, form.errors)
    form = UserRegistrationForm()
    context['form'] = form
    return render(request, 'account_app/register.html', context)


def login_user(request):
    context = {}
    if request.POST:
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('main_app:dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, form.errors)
    form = AuthenticationForm()
    context['form'] = form
    return render(request, 'account_app/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('account_app:login')
