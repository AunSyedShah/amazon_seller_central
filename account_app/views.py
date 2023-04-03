from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def register_user(request):
    context = {}
    form = UserRegistrationForm()
    context['form'] = form
    return render(request, 'account_app/register.html', context)


def login_user(request):
    context = {}
    form = AuthenticationForm()
    context['form'] = form
    return render(request, 'account_app/login.html', context)
