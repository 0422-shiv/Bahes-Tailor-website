# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.ManageProducts.as_view(), name="ManageProducts"),
path('delete-product/', views.DeleteMultiProducts.as_view(), name="DeleteMultiProducts"),

]