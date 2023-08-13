from .simulator.simulation import run_simulation
from .simulator.configuration import configure
from celery import shared_task


@shared_task()
def run_simulation_task(data):
    run_simulation(configure(data))


