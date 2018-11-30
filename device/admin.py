from django.contrib import admin

from .models import SensorType as DeviceSensorType, Sensor as DeviceSensor, Event as DeviceEvent, Setting

admin.site.register(DeviceSensorType)
admin.site.register(DeviceSensor)
admin.site.register(DeviceEvent)
admin.site.register(Setting)