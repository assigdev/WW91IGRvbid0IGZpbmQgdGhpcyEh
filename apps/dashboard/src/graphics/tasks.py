import os

from celery import Celery
from django.db.models.signals import post_save

from graphics.models import Graphic, update_graphic
from graphics.service import update_from_external

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

app = Celery('base')
app.config_from_object('django.conf:settings')


@app.task
def update_graphic_task(graphic_id):
    graphic = Graphic.objects.get(id=graphic_id)
    post_save.disconnect(update_graphic, sender=Graphic)
    update_from_external(graphic)
    post_save.connect(update_graphic, sender=Graphic)
