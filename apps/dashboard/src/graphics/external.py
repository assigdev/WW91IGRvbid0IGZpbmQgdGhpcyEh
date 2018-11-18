from base import settings
import requests
from io import BytesIO
from django.core import files


class ExtSender:
    def __init__(self, data, title):
        self.gen_data_url = settings.GEN_DATA_URL
        self.gen_image_url = settings.GEN_IMAGE_URL
        self.data = data
        self.image_data = {'infile': {'title': {'text': title}}}
        self.fp = BytesIO()

    def _generate_data(self):
        req = requests.post(self.gen_data_url, json=self.data)
        result = req.json()
        self.image_data.update(result)

    def _generate_image(self):
        resp = requests.post(self.gen_image_url, json=self.image_data)
        if resp.status_code != 200:
            raise Exception()
        self.fp.write(resp.content)

    def send(self):
        # self._generate_data()
        # Fixme when generate_date_app complete
        fake_infile = {"xAxis": {"categories": ["Jan", "Feb", "Mar"]}, "series": [{"data": [29.9, 71.5, 106.4]}]}
        self.image_data['infile'].update(fake_infile)
        self._generate_image()

    def get_result_image(self):
        return files.File(self.fp)
