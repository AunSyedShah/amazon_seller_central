from django.shortcuts import render


# Create your views here.
def register_user(request):
    return render(request, 'account_app/register.html')
