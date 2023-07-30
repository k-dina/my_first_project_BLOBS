from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def get_user_name(user) -> str:
    return f'{user.first_name}'

def index(request):
    return render(request, 'index.html')


def saved_simulations(request):
    return render(request, 'saved_simulations.html')


def userspace(request):
    user = request.user
    context = {
        'user_name': get_user_name(user),
    }
    return render(request, 'userspace.html', context=context)


def view_saved_simulation(request):
    return render(request, 'view_saved_simulation.html')


def newsimulation(request):
    return render(request, 'newsimulation.html')


def view_simulation(request):
    return render(request, 'view_simulation.html')


def save_simulation(request):
    return render(request, 'save_simulation.html')
