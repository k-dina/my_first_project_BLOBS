from processor import Processor
import random

def clamp(value, lower, upper) -> int:
    return lower if value < lower else value if value < upper else upper

class FieldProcessor(Processor):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.__field_fertility = configuration['field_fertility']
        self.__exp = configuration['exp']
        self.__field_size = configuration['field_size']

    def process(self, field):
        field = {key: value - 1 if value > 0 else value for (key, value) in field.items()}
        empty_cells = list(filter(lambda x: field[x] == 0, field.keys()))

        food_amount = clamp(round(0.04 * self.__field_size * self.__field_size * self.__field_fertility),
                            0,
                            len(empty_cells))
        new_food = random.sample(list(empty_cells), food_amount)

        field.update({x: self.__exp for x in new_food})

