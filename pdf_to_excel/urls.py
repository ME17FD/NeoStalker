from django.urls import path
from . import views

urlpatterns = [
    path('', views.pdf_to_excel, name='pdf_to_excel'),
    path('rename-columns/', views.rename_columns, name='rename_columns'),
]