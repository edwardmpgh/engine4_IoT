from django.contrib import admin

from .models import Profile, Device, SensorType, Sensor, Event

admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(SensorType)
admin.site.register(Sensor)
admin.site.register(Event)