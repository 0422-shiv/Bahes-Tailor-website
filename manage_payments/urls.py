# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
path('cost', views.ManageCost.as_view(), name="ManageCost"),
path('update-cost/<int:id>', views.UpdateManageCost.as_view(), name="UpdateManageCost"),
path('order', views.ManageOrder.as_view(), name="ManageOrder"),
]