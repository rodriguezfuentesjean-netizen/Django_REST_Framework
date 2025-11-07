from django.contrib import admin
from .models import CityTemperature

@admin.register(CityTemperature)
class CityTemperatureAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'last_updated')
    search_fields = ('city',)

