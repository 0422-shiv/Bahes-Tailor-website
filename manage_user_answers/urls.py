from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.SupplierAnswer.as_view(), name = 'SupplierAnswer'),
    path('customer-answers/', views.CustomerAnswer.as_view(), name = 'CustomerAnswer'),
]