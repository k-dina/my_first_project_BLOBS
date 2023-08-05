from processor import Processor
import numpy as np
import random

# как тут импортировать???
# from simulation import configuration, clamp

# как это нормально положить???

look_around = [(x, y) for x in range(-5, 6) for y in range(-5, 6)]
look_around = sorted(look_around, key=lambda x: max(x))
look_around.remove((0, 0))


def vector_sum(first, second):
    return first[0] + second[0], first[1] + second[1]


def get_vision_field(location, look_around):
    return [vector_sum(x, location) for x in look_around]


def success_prob(blob, other_blob):
    distance = abs((other_blob['vitality'] - blob['vitality']) / 100)
    return 1 - distance - 0.2


def new_blob(blob, other_blob, blobs, other_blobs, configuration):
    i = len(blobs)

    new_blob = {}
    new_blob['id'] = i

    mean = (blob['vitality'] + other_blob['vitality']) / 2
    sd = configuration['SD']
    new_blob['vitality'] = clamp(np.random.normal(mean, sd), 1, 100)

    mean = (blob['charisma'] + other_blob['charisma']) / 2
    new_blob['charisma'] = clamp(np.random.normal(mean, sd), 1, 100)

    new_blob['life'] = 100
    new_blob['speed'] = round((new_blob['life'] + new_blob['vitality']) / 40)  # это поле нужно рассчитывать динамически
    new_blob['freeze'] = 0

    while True:
        location = random.randint(0, 100), random.randint(0, 100)
        # будет ли тут проходиться по ключам???
        if location not in other_blobs:
            new_blob['location'] = location
            break
    other_blobs[new_blob['location']] = new_blob

    blobs[i] = new_blob

    blob['freeze'] = 3
    other_blob['freeze'] = 3


class MatingProcessor(Processor):
    def __init__(self, configuration):
        super().__init__(configuration)

    def process(self, blobs, other_blobs, configuration):
        pairs = {}
        unique_blobs = set()
        for blob in blobs.values():
            unique_blobs += blob['id']
            for location in get_vision_field(blob['location'], look_around):
                if other_blobs[location]:
                    for other_blob in other_blobs[location]:
                        if other_blob['id'] not in unique_blobs:
                            pairs[blob['id'], other_blob['id']] = 0

        for pair in pairs:
            pairs[pair] = success_prob(blobs[pair[0]], blobs[pair[1]])

        pairs = sorted([[key, value] for key, value in pairs.items()], key=lambda x: x[1], reverse=True)
        matched_blobs = set()
        for pair in pairs:
            if set(pair[0]) & matched_blobs:
                pair[1] = 0
            else:
                matched_blobs | set(pair[0])

        pairs = filter(lambda x: x[1], pairs)

        for pair in pairs:
            new_blob(blobs[pair[0]], blobs[pair[1]], blobs, other_blobs, configuration)

