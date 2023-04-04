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
    form = AuthenticationForm()
    context['form'] = form
    return render(request, 'account_app/login.html', context)
