from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path('login', views.Login , name = "login"),
    path('',views.displayscrn,name="display"),
    path('logout/',views.logoutview,name="logout"),
    path('input/',views.addscrn,name="input"),
    path('excel/',views.upload_excel ,name="upload_excel"),
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
    
]
