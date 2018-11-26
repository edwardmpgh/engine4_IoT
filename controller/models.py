from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

DB_PREFIX = 'e4iot_'


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


THEME_CHOICES = (
    ('s', 'Default Theme'),
    ('d', 'Dark Theme'),
    ('c', 'High Contrast Theme'),
)


class Profile(CommonField):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(blank=True, null=True)
    theme = models.CharField(max_length=1, choices=THEME_CHOICES, default='s')
    alert_email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = DB_PREFIX + 'profile'


# # Create or update profile when user instance is created or updated
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.Profile.save()


class Device(CommonField):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


SENSOR_DATA_TYPES = (
    ('i', 'integer'),
    ('f', 'float'),
    ('b', 'boolean'),
    ('s', 'string'),
)


class SensorType(CommonField):
    name = models.CharField(max_length=50)
    data_type = models.CharField(max_length=1, choices=SENSOR_DATA_TYPES)


class Sensor(CommonField):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(SensorType, on_delete=models.CASCADE)


class Channel(CommonField):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=15)
