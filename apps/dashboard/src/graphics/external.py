from base import settings
import requests
from io import BytesIO
from django.core import files
from datetime import datetime
from django.utils import timezone


class ExtSenderException(Exception):
    '''Exception class for ExtSender'''


class ExtSender:
    def __init__(self, data, title):
        self.gen_data_url = settings.GEN_DATA_URL
        self.gen_image_url = settings.GEN_IMAGE_URL
        self.now = datetime.now(tz=timezone.get_current_timezone())
        data['now'] = self.now.strftime('%d.%m.%y %H:%M:%S.%f')
        self.data = data
        self.image_data = {
            'infile': {
                'title': {'text': title},
                'xAxis': {'categories': []}, 'series': []
            }
        }
        self.fp = BytesIO()

    def _generate_data(self):
        resp = requests.post(self.gen_data_url, json=self.data)
        if resp.status_code != 200:
            if resp.status_code == 400:
                error = resp.json()['error']
                error_text = f'Generate data error: {error}'
            else:
                error_text = 'Generate data error'
            raise ExtSenderException(error_text)
        result = resp.json()
        self.image_data['infile']['xAxis']['categories'] = result['result']['categories']
        self.image_data['infile']['series'] = [{'data': result['result']['data']}]

    def _generate_image(self):
        resp = requests.post(self.gen_image_url, json=self.image_data)
        if resp.status_code != 200:
            raise ExtSenderException('Generate image error')
        self.fp.write(resp.content)

    def send(self):
        self._generate_data()
        self._generate_image()

    def get_result_image(self):
        return files.File(self.fp)

    def get_now(self):
        return self.now
