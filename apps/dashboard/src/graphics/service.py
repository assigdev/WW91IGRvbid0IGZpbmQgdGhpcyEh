from graphics.external import ExtSender, ExtSenderException


def update_from_external(obj):
    sender = ExtSender(obj.get_data_dict(), obj.get_formula_display())
    now = sender.get_now()
    try:
        sender.send()
    except ExtSenderException as e:
        obj.error = str(e)
    else:
        image_file = sender.get_result_image()
        obj.image.save(f'{now}.png', image_file)
        obj.error = ''
    obj.date = now
    obj.save()
