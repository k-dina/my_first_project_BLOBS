# start simulation
import random
import numpy as np
from configuration import configuration

from processors.health_speed_processor import HealthSpeedProcessor
from processors.mating_processor import MatingProcessor
from processors.harvesting_processor import HarvestingProcessor

# куда сложить функции, чтобы их было удобно везде импортировать? пока что я их просто вот так
# в каждом файле оставила, где они нужны
def clamp(value, lower, upper) -> int:
    return lower if value < lower else value if value < upper else upper


# тут мы прям вот так делаем первые 100 блобсов
other_blobs = {}
blobs = {}
blob_location = set()
for i in range(100):
    blob = {}
    blob['id'] = i
    blob['vitality'] = round(clamp(np.random.normal(configuration['vitality'], configuration['sd']), 1, 100))
    blob['charisma'] = round(clamp(np.random.normal(configuration['charisma'], configuration['sd']), 1, 100))
    blob['life'] = 100
    blob['speed'] = round((blob['life'] + blob['vitality']) / 40)
    blob['freeze'] = 0
    while True:
        location = random.randint(0, 100), random.randint(0, 100)
        if location not in blob_location:
            blob['location'] = location
            break
    other_blobs[blob['location']] = [blob]
    blobs[i] = blob

# тут будем хранить данные о поле. ключи - клетки поля. числа - состояния. при данных значениях параметра
# 3 - свежая еда, 2 - не очень свежая еда, 1 - скоро испортится, 0 - нет еды

field = dict.fromkeys([(i, j) for i in range(configuration['field_size'])
                       for j in range(configuration['field_size'])], 0)




health_processor = HealthSpeedProcessor(configuration)
harvesting_processor = HarvestingProcessor(configuration)
mating_processor = MatingProcessor(configuration)

