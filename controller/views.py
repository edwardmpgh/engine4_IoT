from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Sensor

# JSON responses for charts


def get_sensor_detail(request, sensor_id):

    sensor_data = Sensor.objects.get(id=sensor_id)

    data = {
        'value': sensor_data.last_alert_value,
        'date': sensor_data.last_alert,
        'alert_state': sensor_data.alert,
    }
    return JsonResponse(data)
