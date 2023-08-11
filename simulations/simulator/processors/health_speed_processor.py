from .processor import Processor


class HealthSpeedProcessor(Processor):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.__life_decrease = configuration['life_decrease']

    def process(self, blobs, blobs_on_field):
        for blob_id in blobs:
            blob = blobs[blob_id]
            blob['life'] -= self.__life_decrease
            if blob['life'] <= 0:
                blobs.pop(blobs['id'])
                blobs_on_field[blob['location']].remove(blob['id'])
            blob['speed'] = round((blob['life'] + blob['vitality']) / 40)

