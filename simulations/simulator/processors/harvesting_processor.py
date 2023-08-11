from .processor import Processor
from .functions import *


class HarvestingProcessor(Processor):
    look_around = LOOK_AROUND

    def __init__(self, configuration):
        super().__init__(configuration)
        self.__life_increase = configuration['life_increase']
        self.__field_size = configuration['field_size']

    def process(self, field, blobs, blobs_on_field):
        for blob_id in blobs:
            self.__find_food(blob_id, field, blobs, blobs_on_field)
        for location in field:
            if field[location]:
                if blobs_on_field[location]:
                    winner = self.__fight_for_food(blobs_on_field[location], blobs)
                    if winner:
                        self.__eat_food(winner, blobs, location, field)

    def __fight_for_food(self, blob_id_list, blobs):

        distribution = self.__success_prob(blob_id_list, blobs)
        remaining_blobs = []
        for blob_id in distribution:
            if np.random.binomial(1, distribution[blob_id]):
                remaining_blobs.append(blob_id)
        distribution = self.__success_prob(remaining_blobs, blobs)
        if remaining_blobs:
            return int(np.random.choice(remaining_blobs, size=1, p=list(distribution.values())))

    def __eat_food(self, blob_id, blobs, food_location, field):

        blobs[blob_id]['life'] = min(100, self.__life_increase)
        field[food_location] = 0

    def __find_food(self, blob_id, field, blobs, blobs_on_field):
        blob = blobs[blob_id]
        food = []
        nearest_circle = None

        for goal in crop_area(get_vision_field(blob['location'], HarvestingProcessor.look_around), self.__field_size):
            if field[goal] != 0:
                circle = get_circle(vector_diff(goal, blob['location']))  # Здесь нужно рассчитать значение "circle"

                if nearest_circle is None:
                    nearest_circle = circle
                    food = [goal]

                elif circle == nearest_circle:
                    food.append(goal)

                elif circle > nearest_circle:
                    break

        if food:
            food_indices = list(range(len(food)))
            random_index = np.random.choice(food_indices)
            goal = food[random_index]
            blobs_on_field[blob['location']].remove(blob_id)
            blob['location'] = vector_sum(blob['location'],
                                          clamp_2d(vector_diff(goal, blob['location']), blob['speed']))
            blobs_on_field[blob['location']].append(blob['id'])

    @staticmethod
    def __success_prob(args, blobs):
        rez = {blobs[arg]['id']: (blobs[arg]['life'] + blobs[arg]['vitality'] + blobs[arg]['charisma']) for arg in
               args}
        return {blob_id: prob / sum(rez.values()) for blob_id, prob in rez.items()}
