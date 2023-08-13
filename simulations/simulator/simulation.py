# start simulation
import random
import numpy as np
from .mongo_db import save_snapshot, get_db
from .processors.functions import clamp
import uuid

from .processors.field_processor import FieldProcessor
from .processors.health_speed_processor import HealthSpeedProcessor
from .processors.mating_processor import MatingProcessor
from .processors.harvesting_processor import HarvestingProcessor



def run_simulation(configuration):
    simulation_id = str(uuid.uuid4())

    blobs_on_field = {(i, j): [] for i in range(configuration['field_size']) for j in
                      range(configuration['field_size'])}

    blobs = {}

    for i in range(100):
        blob = {}
        blob['id'] = i
        blob['vitality'] = round(clamp(np.random.normal(configuration['vitality'], configuration['sd']), 1, 100))
        blob['charisma'] = round(clamp(np.random.normal(configuration['charisma'], configuration['sd']), 1, 100))
        blob['life'] = 100
        blob['speed'] = round((blob['life'] + blob['vitality']) / 40)
        blob['freeze'] = 0
        blob['location'] = random.randint(0, 99), random.randint(0, 99)
        blobs_on_field[blob['location']].append(i)
        blobs[i] = blob

    field = {(i, j): 0 for i in range(configuration['field_size'])
             for j in range(configuration['field_size'])}

    health_processor = HealthSpeedProcessor(configuration)
    mating_processor = MatingProcessor(configuration)
    field_processor = FieldProcessor(configuration)
    harvesting_processor = HarvestingProcessor(configuration)

    for i in range(10):
        if not (i % 24):
            field_processor.exp(field)
            field.update(field_processor.grow_food(field))
        health_processor.process(blobs, blobs_on_field)
        mating_processor.process(blobs, blobs_on_field)
        harvesting_processor.process(field, blobs, blobs_on_field)
        db = get_db()
        save_snapshot(db, simulation_id, {
            'step': i,
            'blobs': str(blobs),
            'field': str(field),
            'blobs_on_field': str(blobs_on_field),
        })
