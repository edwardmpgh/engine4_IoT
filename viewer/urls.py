from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='viewer_index'),
    path('login/', views.login_base, name='login'),
    path('logout/', views.logout_base, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('change_setting/', views.change_setting, name='change_setting'),
]
