from .processor import Processor
from .functions import clamp
import random


class FieldProcessor(Processor):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.__field_fertility = configuration['field_fertility']
        self.__exp = configuration['exp']
        self.__field_size = configuration['field_size']

    def grow_food(self, field):
        empty_cells = list(filter(lambda x: field[x] == 0, field.keys()))

        food_amount = clamp(round(0.04 * self.__field_size * self.__field_size * self.__field_fertility), 0,
                            len(empty_cells))
        new_food = random.sample(list(empty_cells), food_amount)

        return {x: self.__exp for x in new_food}

    def exp(self, field):
        for key in field:
            if field[key] > 0:
                field[key] -= 1
