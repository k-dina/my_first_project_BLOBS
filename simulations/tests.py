from django.test import TestCase

# Create your tests here.
from tasks import run_simulation_task
from simulator.configuration import DEFAULT_CONFIGURATION

run_simulation_task(DEFAULT_CONFIGURATION)