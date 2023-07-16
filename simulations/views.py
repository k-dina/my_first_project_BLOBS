from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def new_user(request):
    return render(request, 'new_user.html')


def saved_simulations(request):
    return render(request, 'saved_simulations.html')


def userspace(request):
    return render(request, 'userspace.html')


def view_saved_simulation(request):
    return render(request, 'view_saved_simulation.html')


def newsimulation(request):
    return render(request, 'newsimulation.html')


def new_anonymous_simulation(request):
    return render(request, 'new_anonymous_simulation.html')


def view_simulation(request):
    return render(request, 'view_simulation.html')


def save_simulation(request):
    return render(request, 'save_simulation.html')
