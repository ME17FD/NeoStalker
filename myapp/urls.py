from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path('login', views.Login , name = "login"),
    path('',views.displayscrn,name="display"),
    path('logout/',views.logoutview,name="logout"),
    path('input/',views.addscrn,name="input")
    
]
