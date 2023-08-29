from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from celery.result import AsyncResult

from mongoengine import connect

from .forms import SimulationForm
from .tasks import run_simulation_task
from .simulator.simulation import initialize_simulation
from .simulator.configuration import *
from .simulator.models import Snapshot

import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

connect('simulations', host='mongo', port=27017)


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
            simulation_id = initialize_simulation(configuration)
            task = run_simulation_task.apply_async(args=[simulation_id, 0])
            task_id = task.id
            logging.debug(task_id)
            return HttpResponseRedirect(f'/view_simulation/{simulation_id}/{task_id}/')

        errors = 'The parameters are not filled or filled incorrectly! ' \
                 'Read the instructions carefully and resubmit the form'

    else:
        form = SimulationForm()

    return render(request, 'newsimulation.html', {'form': form, 'next': next_page, 'errors': errors})


def get_snapshots(request, id, step):
    new_data = Snapshot.objects(simulation_id=id, step__gte=step)
    data = {}
    for snapshot in new_data:
        data[snapshot.step] = len(snapshot.blobs)
    return JsonResponse(data, status=200)


def resume_simulation(request, id, step):
    task = run_simulation_task.apply_async(args=[id, step - 1])
    return JsonResponse({'new_task_id': task.id}, status=200)


def task_isready(request, task_id):
    res = AsyncResult(task_id)
    return JsonResponse({'task_is_ready': res.ready()})


def view_simulation(request, id, task_id):
    last_step = len(Snapshot.objects(simulation_id=id))
    return render(request, 'view_simulation.html', {'simulation_id': id, 'last_step': last_step, 'current_task_id': task_id},)


def save_simulation(request):
    return render(request, 'save_simulation.html')
