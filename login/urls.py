from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('loadLogin', views.loadLogin, name='loadLogin'),
    path('loadRegister', views.loadRegister, name='loadRegister'),
    path('loadOTP', views.loadOTP, name='loadOTP'),
    path('loadDashbord', views.loadDashbord, name='loadDashbord'),

    path('insertLogin', views.insertLogin, name='insertLogin'),
    path('insertRegister', views.insertRegister, name='insertRegister'),
    path('insertOTP', views.insertOTP, name='insertOTP'),

    path('logout', views.logout, name='logout'),

]
