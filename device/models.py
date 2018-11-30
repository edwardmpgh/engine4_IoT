from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

DB_PREFIX = 'e4iotd_'


class CommonField(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    trash = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def is_active(self):
        return self.active

    def is_trash(self):
        return self.trash

    def flip_active_flag(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def flip_trash_flag(self):
        if self.trash:
            self.trash = False
        else:
            self.trash = True


class Setting(CommonField):
    setting_key = models.CharField(max_length=50)
    setting_value = models.CharField(max_length=255)

    def __str__(self):
        return '%s: %s' % (self.setting_key, self.setting_value)

    class Meta:
        db_table = DB_PREFIX + 'setting'


class SensorType(CommonField):
    name = models.CharField(max_length=50)
    alert_low = models.FloatField(blank=True, null=True)
    alert_high = models.FloatField(blank=True, null=True)
    sensor_brand = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = DB_PREFIX + 'sensor_type'


class Sensor(CommonField):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    alert = models.BooleanField(default=False)
    last_alert_value = models.FloatField(blank=True, null=True)
    last_alert = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = DB_PREFIX + 'sensor'


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=5)

    def __str__(self):
        return '%s: %s' % (self.created, self.sensor.name)

    class Meta:
        db_table = DB_PREFIX + 'event'
