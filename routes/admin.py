from django.contrib import admin
from .models import *

class RouteAdmin(admin.ModelAdmin):
    readonly_fields = [
        'distance',
        'rate'
    ]


admin.site.register(Route, RouteAdmin)
