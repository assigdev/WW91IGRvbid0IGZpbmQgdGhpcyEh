from django.contrib import admin
from graphics.models import Graphic
from django.utils.html import mark_safe
from graphics.tasks import update_graphic_task


@admin.register(Graphic)
class GraphicAdmin(admin.ModelAdmin):

    def get_graphic(self, obj):
        if not obj.error and obj.image:
            return mark_safe(f'<a href="{obj.image.url}" target="_blank">'
                             f'<img src="{obj.image.url}" width="300" height="180" /></a>')
        return obj.error or 'Ожидается'

    get_graphic.short_description = 'График'
    get_graphic.allow_tags = True

    def update_graphics(self, request, queryset):
        for obj in queryset:
            update_graphic_task.delay(obj.id)
        self.message_user(request, f"Графики в количестве {queryset.count()} объектов обновляются")

    update_graphics.short_description = 'Обновить'
    update_graphics.allow_tags = True

    list_display = ('formula', 'get_graphic', 'interval', 'dt', 'date')
    readonly_fields = ('get_graphic',)
    fields = ('formula', 'interval', 'dt')
    actions = ['update_graphics']
