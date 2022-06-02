from django.contrib import admin
from .models import Batch, ColorData


@admin.register(ColorData)
class ColorDataAdmin(admin.ModelAdmin):
    list_display = ('batch', 'timestamp', 'category', 'color_sheet')
    list_filter = ('category',)


admin.site.register(Batch)
#admin.site.register(ColorData)
