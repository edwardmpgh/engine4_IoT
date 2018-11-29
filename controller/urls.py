from django.urls import path

from . import views

urlpatterns = [
    path('sensor/<int:sensor_id>/', views.get_sensor_detail, name='get_sensor_detail'),
]
