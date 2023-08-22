from .processor import Processor


class HealthSpeedProcessor(Processor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def process(blobs, blobs_on_field, configuration):
        for blob_id in blobs:
            blob = blobs[blob_id]
            blob['life'] -= configuration.life_decrease
            if blob['life'] <= 0:
                blobs.pop(blobs['id'])
                blobs_on_field[blob['location']].remove(blob['id'])
            blob['speed'] = round((blob['life'] + blob['vitality']) / 40)

