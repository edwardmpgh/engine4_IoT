from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='device_index'),
    path('register/', views.register_device, name='register_device')
]
