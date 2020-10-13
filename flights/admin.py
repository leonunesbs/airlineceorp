from django.contrib import admin
from .models import *


class RepeatAdmin(admin.ModelAdmin):
    pass


class FlightAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'repeat'
    ]


admin.site.register(Flight, FlightAdmin)
admin.site.register(Repeat, RepeatAdmin)
