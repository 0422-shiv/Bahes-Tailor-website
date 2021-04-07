# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.ManageCms.as_view(), name="ManageCms"),
path('edit/<int:id>', views.EditCms.as_view(), name="EditCms"),

]