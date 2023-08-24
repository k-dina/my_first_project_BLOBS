from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from celery.result import AsyncResult
import json
import time

import pymongo
from mongoengine import connect

from .forms import SimulationForm
from .tasks import run_simulation_task
from .simulator.simulation import initialize_simulation
from .simulator.configuration import *
from .simulator.models import Simulation, Snapshot, Blob


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

            # return HttpResponseRedirect(f'/view_simulation/{task_id}/')
            return HttpResponseRedirect(f'/view_simulation/{simulation_id}/')

        errors = 'The parameters are not filled or filled incorrectly! ' \
                 'Read the instructions carefully and resubmit the form'

    else:
        form = SimulationForm()

    return render(request, 'newsimulation.html', {'form': form, 'next': next_page, 'errors': errors})


def get_snapshots(request, id, step):
    simulation_id = id
    connect('simulations', host='mongo', port=27017)
    simulation = Simulation.objects.get(simulation_id=simulation_id)
    new_data = simulation.snapshots[step::]
    data = {}
    for snapshot in new_data:
        data[snapshot.step] = len(snapshot.blobs)
    return JsonResponse(data, status=200)


def view_simulation(request, id):
    # task_id = id
    # task_result = AsyncResult(task_id)

    # result = {
    #     "task_id": task_id,
    #     "task_status": task_result.status,
    #     "task_result": task_result.result
    # }

    # return JsonResponse(data, status=200)
    return render(request, 'view_simulation.html', {'simulation_id': id, 'last_step': 0})




def save_simulation(request):
    return render(request, 'save_simulation.html')
