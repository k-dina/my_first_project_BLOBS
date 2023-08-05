import random

from processor import Processor
import numpy as np
import math


# где хранить все эти функции?

def clamp(value, lower, upper) -> int:
    return lower if value < lower else value if value < upper else upper


def get_circle(vector):
    return int(max(abs(floor(vector[0])), abs(floor(vector[1]))))


def floor(value):
    return math.copysign(math.floor(abs(value)), value)


def lerp(v1, v2, time):
    return v1 * (1 - time) + v2 * time


def vector_sum(first, second):
    return first[0] + second[0], first[1] + second[1]


def get_vector(goal, circle):
    time = 0
    while True:
        time += 0.2
        result = lerp(np.array((0, 0)), np.array(goal), time)
        print('time: ', time)
        print('result: ', result)
        print('get circle:', get_circle(result))
        if get_circle(result) == circle:
            return floor(result[0]), floor(result[1])


def clamp_2d(goal, speed):
    distance = get_circle(goal) - speed
    if distance <= 0:
        return goal
    return get_vector(goal[1] / goal[0], speed)


def find_food(blob, field, look_around, other_blobs):
    location = blob['location']
    food = []
    for i in look_around:
        goal = field[vector_sum(location, i)]
        if goal != 0:
            circle = get_circle(goal)
            food.append(circle)
            if circle > food[0]:
                break
            food.append(goal)
    food.pop(0)
    goal = np.random.choice(food, size=1, p=[1 / len(food)] * len(food))
    other_blobs[blob['location']].remove(blob['id'])
    blob['location'] += clamp_2d(goal, blob['speed'])
    other_blobs[blob['location']].append(blob['id'])

    # а что елси блобс не нашел еду??? просто стоит и ждет, пока в поле зрения появится новая еда


def success_prob(args):
    factor = sum([arg['life'] + arg['vitality'] + arg['charisma'] for arg in args])
    return {arg: (arg['life'] + arg['vitality'] + arg['charisma']) / factor / len(args) for arg in args}


def eat_food(blob_id, blobs, food_location, field, life_increase):
    blobs[blob_id] += life_increase
    field[food_location] = 0


def fight_for_food(blob_list):
    distribution = success_prob(blob_list)
    remaining_blobs = []
    for blob_id in distribution:
        if np.random.binomial(1, distribution[blob_id]):
            remaining_blobs.append(blob_id)
    distribution = success_prob(remaining_blobs)
    return np.random.choice(remaining_blobs, size=1, p=distribution.values())


# куда это?????

look_around = [(x, y) for x in range(-5, 6) for y in range(-5, 6)]
look_around = sorted(look_around, key=lambda x: get_circle(x))
look_around.remove((0, 0))


class HarvestingProcessor(Processor):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.__life_increase = configuration['life_increase']

    def process(self, field, blobs, other_blobs, look_around):
        for blob in blobs:
            find_food(blob, field, look_around, other_blobs)
        for location in field:
            if field[location]:
                if other_blobs[location]:
                    winner = fight_for_food(other_blobs[location])
                    eat_food(winner, blobs, location, field, self.__life_increase)


