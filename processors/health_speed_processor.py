from processor import Processor


class HealthSpeedProcessor(Processor):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.__life_decrease = configuration['life_decrease']

    def process(self, blobs, other_blobs):
        for blob in blobs:
            blob['life'] -= self.__life_decrease
            if blob['life'] <= 0:
                blobs.pop(int(blob['id']))
                other_blobs[blob['location']].remove(blob['id'])
            blob['speed'] = round((blob['life'] + blob['vitality']) / 40)
