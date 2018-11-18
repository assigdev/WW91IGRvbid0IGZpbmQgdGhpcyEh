from django.contrib import admin
from graphics.models import Graphic
from django.utils.html import mark_safe


@admin.register(Graphic)
class GraphicAdmin(admin.ModelAdmin):

    def get_graphic(self, obj):
        if not obj.error and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" height="180" />')
        return obj.error or 'Ожидается'

    get_graphic.short_description = 'График'
    get_graphic.allow_tags = True

    list_display = ('formula', 'get_graphic', 'interval', 'dt', 'date')
    readonly_fields = ('get_graphic',)
    fields = ('formula', 'interval', 'dt')
