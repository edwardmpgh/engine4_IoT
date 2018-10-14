from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='viewer_index'),
    path('change_setting/', views.change_setting, name='change_setting'),
]
