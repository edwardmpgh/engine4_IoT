from random import randint
import random
import string

from django.shortcuts import render, reverse
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Sensor, SensorType, Event, Setting


# get system settings
def get_setting_value(key_value):

    settings = Setting.objects.all()
    setting_value = ''

    for s in settings:
        if s.setting_key == key_value:
            setting_value = s.setting_value

    return setting_value


# get system settings
def set_setting_value(key_value, setting_value):

    settings = Setting.objects.all()

    for s in settings:
        if s.setting_key == key_value:
            s.setting_value = setting_value
            s.save()


# return a list of the installed expected sensors
def get_system_sensors():
    # this is where the Raspberry Pi sensor discovery code will go

    # for testing, we will simulate sensor discovery
    # this would normally be build from the system sensor discovery process
    sensors = (
        'DS18B20',
        'MQ-2',
        'MG811',
        'MQ307A',
    )

    return sensors


def add_new_sensors():
    # get system sensors
    sensors = get_system_sensors()
    # get the sensor type info for the supported system sensors not in the sensor table
    current_sensors = Sensor.objects.filter(trash=False, active=True).values_list('type__sensor_brand')
    supported_system_sensors = SensorType.objects.filter(trash=False, active=True, sensor_brand__in=sensors).exclude(
        sensor_brand__in=current_sensors)

    # add the new sensors to the sensor table
    if supported_system_sensors:
        for sensor_type in supported_system_sensors:
            new_sensor = Sensor(type=sensor_type, name=sensor_type.name)
            new_sensor.save()


def log_event(sensor, value, event_type):
    Event(sensor=sensor, value=value, event_type=event_type).save()


# read the system sensors
def read_sensors():
    # this is test code to simulate sensor reading
    # get sensors
    sensors = Sensor.objects.filter(trash=False, active=True)
    for sensor in sensors:
        if sensor.type.name == 'Temperature Sensor':
            sensor.last_alert_value = randint(68, 70)
        elif sensor.type.name == 'Smoke Detector':
            sensor.last_alert_value = randint(500, 1500)
        elif sensor.type.name == 'CO2 Detector':
            sensor.last_alert_value = randint(100, 7000)
        else:
            # CO detector
            sensor.last_alert_value = randint(0, 70)

        if sensor.type.alert_low:
            if sensor.type.alert_low >= sensor.last_alert_value:
                sensor.alert = True
            else:
                sensor.alert = False
        sensor.save()
        log_event(sensor, sensor.last_alert_value, 'SR')


def index(request):

    # add new sensors if needed
    add_new_sensors()

    # do a sensor reading
    read_sensors()

    # get sensors
    sensors = Sensor.objects.filter(trash=False, active=True)

    # build page data
    context = dict(
        sensors=sensors
    )

    return render(request, 'device/index.html', context)

    # show the sensors


def register_device(request):

    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    set_setting_value('device_registration_code', code)

    context = dict(
        code=code,
    )

    return render(request, 'device/register_device.html', context)
