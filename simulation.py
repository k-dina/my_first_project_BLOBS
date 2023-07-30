# start simulation
import random
import numpy as np


# я не поняла, как лучше хранить и изменять информацию. Я знаю, что на данный момент мои функции не
# поменяют состояние! А как сделать, чтобы красиво меняли?

# тут я пишу некоторые функции, которые потом часто использую

def clamp(value, lower, upper) -> int:
    return lower if value < lower else value if value < upper else upper


# здесь цель - ограницить движение блобса его скоростью. ему надо в goal. но если скорость не позволяет,
# он идет в нужную сторону, но не доходит до цели. пространство представлено в виде "колец" клеток.

def clamp_2d(goal, speed):
    distance = max(goal) - speed
    if distance == 0:
        return goal
    else:
        return goal - (distance, distance)


# initial parameters

field_fertility = 10
vitality = 70
charisma = 50
FIELD_SIZE = 100
BEST_BEFORE = 3
SD = 1

# тут мы прям вот так делаем первые 100 блобсов
other_blobs = {}
blobs = {}
blob_location = set()
for i in range(100):
    blob = {}
    blob['id'] = i
    blob['vitality'] = round(clamp(np.random.normal(vitality, SD), 1, 100))
    blob['charisma'] = round(clamp(np.random.normal(charisma, SD), 1, 100))
    blob['life'] = 100
    blob['speed'] = round((blob['life'] + blob['vitality']) / 40)  # это поле нужно рассчитывать динамически
    blob['freeze'] = 0
    while True:
        location = random.randint(0, 100), random.randint(0, 100)
        if location not in blob_location:
            blob['location'] = location
            break
    other_blobs[blob['location']] = blob

    blobs[i] = blob

print(blobs[3])

# тут будем хранить данные о поле. ключи - клетки поля. числа - состояния. при данных значениях параметра
# 3 - свежая еда, 2 - не очень свежая еда, 1 - скоро испортится, 0 - нет еды

field = dict.fromkeys([(i, j) for i in range(FIELD_SIZE) for j in range(FIELD_SIZE)], 0)


# эта функция обновляет еду на поле, учитывая ее срок годности и плодоносность поля

def grow_food(field, field_fertility):
    global BEST_BEFORE

    field = {key: value - 1 if value > 0 else value for (key, value) in field.items()}
    empty_cells = list(filter(lambda x: field[x] == 0, field.keys()))

    food_amount = clamp(round(0.04 * FIELD_SIZE * FIELD_SIZE * field_fertility), 0, len(empty_cells))
    new_food = random.sample(list(empty_cells), food_amount)

    field.update({x: BEST_BEFORE for x in new_food})
    return field


# порядок обхода при просмотре блобсом окружеющих клеток поля

look_around = [(x, y) for x in range(-4, 5) for y in range(-4, 5)]
look_around = sorted(look_around, key=lambda x: abs(x[0]) + abs(x[1]))
look_around.remove((0, 0))

print(look_around)


# тут блобс ищет еду
def find_food(blob, field):
    location = blob['location']
    for i in look_around:
        goal = field[location + i]
        if goal != 0:
            blob['location'] += clamp_2d(goal, blob['speed'])


# тут только с точки зрения одного из блобсов. Как согласовать? как сделать, чтобы они не ломались?
# на данный момент ниче не заработает

def find_mate(blob, other_blobs):
    for i in look_around:
        other_blob = other_blobs[location + i]
        if other_blob != 0:
            distance = (other_blob['vitality'] - blob['vitality']) / 100
            if other_blob['life'] >= 70 and distance >= 0:
                if np.random.binomial(1 - distance - 0.2, distance + 0.2, size=1):
                    blob['location'] = other_blob['location']
                    blob['freeze'] = 3
                    other_blob['freeze'] = 3
                    if blob['life'] + other_blob['life'] >= 150:
                        new_blob(blob, other_blob)


# блобс есть еду и клетка поля очищается
def eat(blob, food, field):
    field[food] == 0
    blob['life'] = clamp(blob['life'] + 30, 0, 100)


# рождается новый блобс
def new_blob(blob, other_blob):
    global blobs
    global other_blobs
    global SD
    i = len(blobs)

    new_blob = {}
    new_blob['id'] = i

    mean = (blob['vitality'] + other_blob['vitality']) / 2
    sd = SD
    new_blob['vitality'] = clamp(np.random.normal(mean, sd), 1, 100)

    mean = (blob['charisma'] + other_blob['charisma']) / 2
    new_blob['charisma'] = clamp(np.random.normal(mean, sd), 1, 100)

    new_blob['life'] = 100
    new_blob['speed'] = round((new_blob['life'] + new_blob['vitality']) / 40)  # это поле нужно рассчитывать динамически
    new_blob['freeze'] = 0

    while True:
        location = random.randint(0, 100), random.randint(0, 100)
        if location not in blob_location:
            new_blob['location'] = location
            blob_location.add(location)
            break
    other_blobs[new_blob['location']] = new_blob

    blobs[i] = new_blob
