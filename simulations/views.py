from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import SimulationForm
from .tasks import run_simulation_task
from .simulator.configuration import *
from celery.result import AsyncResult



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
    next_page = None
    errors = None

    if request.method == 'GET':
        next_page = request.GET.get('next')
        form = SimulationForm()

    elif request.method == 'POST':
        form = SimulationForm(request.POST)

        if form.is_valid():

            configuration = configure(form.cleaned_data)
            task = run_simulation_task.apply_async(args=[configuration])
            task_id = task.id
            return HttpResponseRedirect(f'/view_simulation/{task_id}/')

        errors = 'Fill the parameters!'

    else:
        form = SimulationForm()

    return render(request, 'newsimulation.html', {'form': form, 'next': next_page, 'errors': errors})


def view_simulation(request, id):
    #task_id = request.GET.get('task_id')
    task_id = id
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)
    #return render(request, 'view_simulation.html')


def save_simulation(request):
    return render(request, 'save_simulation.html')
