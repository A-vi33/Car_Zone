from django.shortcuts import render

from .forms import RegisterForm

def registerUser(request):
    form = RegisterForm()
    context = {
        'form' : form
    }
    return render(request, 'users/register.html', context)
