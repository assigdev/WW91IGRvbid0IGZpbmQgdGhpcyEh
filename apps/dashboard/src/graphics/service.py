from datetime import datetime
from django.utils import timezone
from graphics.external import ExtSender


def update_from_external(obj):
    sender = ExtSender(obj.get_data_dict(), obj.get_formula_display())
    sender.send()
    image_file = sender.get_result_image()
    now = datetime.now(tz=timezone.get_current_timezone())
    obj.image.save(f'{now}.png', image_file)
    obj.date = now
    obj.save(update_fields={'date'})
