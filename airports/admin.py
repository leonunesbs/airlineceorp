from django.contrib import admin
from .models import *

class AirportAdmin(admin.ModelAdmin):
    list_display = [
        'icao',
        'name',
        'city',
        'uf',
        'latitude',
        'longitude',
        'operation_mode',
        'length',
        'width',
        'rate',
    ]
    search_fields = [
        'icao',
        'city',
        'uf',
    ]
    list_filter = [
        'uf',
        'operation_mode'
    ]
    ordering = ['icao']


admin.site.register(Airport, AirportAdmin)
admin.site.register(AirportLicense)
