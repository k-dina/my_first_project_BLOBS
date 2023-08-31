from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm, NewUserForm

import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)


# Create your views here.
def login(request: HttpRequest):
    next_page = None
    errors = None

    if request.method == 'GET':
        next_page = request.GET.get('next')
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect('/userspace')
                else:
                    errors = 'Username is inactive!'
            else:
                errors = 'Username or password are invalid!'
        else:
            errors = 'Fill both username and password!'
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'next': next_page, 'errors': errors})


def new_user(request):
    return render(request, 'new_user.html')


def new_user(request):
    errors = {}
    form = NewUserForm()

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('userspace')

        errors = form.errors
    return render(request, 'new_user.html', context={'form': form, 'errors': errors})


def logout_view(request):
    django_logout(request)
    return redirect('simulations')