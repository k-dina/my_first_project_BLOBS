from .processor import Processor
from .functions import *  # todo: конкретные функции


class MatingProcessor(Processor):
    look_around = LOOK_AROUND

    def __init__(self, configuration):
        super().__init__(configuration)
        self.__sd = configuration['sd']
        self.__prob_decrease = configuration['prob_decrease']
        self.__field_size = configuration['field_size']

    def process(self, blobs, blobs_on_field):

        pairs = self.__collect_pairs(blobs, blobs_on_field)

        for pair in pairs:
            pairs[pair] = self.__success_prob(blobs[pair[0]], blobs[pair[1]])

        pairs = self.__match_blobs(pairs)

        for pair in pairs:
            self.__new_blob(blobs[pair[0][0]], blobs[pair[0][1]], blobs, blobs_on_field)

    def __collect_pairs(self, blobs, blobs_on_field):
        pairs = {}

        for blob in blobs.values():

            for location in crop_area(get_vision_field(blob['location'], MatingProcessor.look_around),
                                      self.__field_size):
                if blobs_on_field[location]:
                    for other_blob in blobs_on_field[location]:
                        pair = tuple(sorted([blob['id'], other_blob]))
                        pairs[pair] = 0
        return pairs

    def __match_blobs(self, pairs):
        pairs = sorted([[key, value] for key, value in pairs.items()], key=lambda x: x[1], reverse=True)
        matched_blobs = set()

        for pair in pairs:
            if set(pair[0]) & matched_blobs:
                pair[1] = 0
            else:
                matched_blobs = matched_blobs | set(pair[0])

        pairs = filter(lambda x: x[1], pairs)
        return pairs

    def __new_blob(self, blob, other_blob, blobs, blobs_on_field):
        i = len(blobs)

        new_blob = {}
        new_blob['id'] = i

        mean = (blob['vitality'] + other_blob['vitality']) / 2
        sd = self.__sd
        new_blob['vitality'] = clamp(np.random.normal(mean, sd), 1, 100)

        mean = (blob['charisma'] + other_blob['charisma']) / 2
        new_blob['charisma'] = clamp(np.random.normal(mean, sd), 1, 100)

        new_blob['life'] = 100
        new_blob['speed'] = round((new_blob['life'] + new_blob['vitality']) / 40)
        new_blob['freeze'] = 3

        new_blob['location'] = blob['location']
        blobs_on_field[new_blob['location']].append(new_blob['id'])

        blobs[i] = new_blob

        blob['freeze'] = 3
        other_blob['freeze'] = 3

        return new_blob

    def __success_prob(self, blob, other_blob):
        distance = abs((other_blob['vitality'] - blob['vitality']) / 100)
        return 1 - distance - self.__prob_decrease
