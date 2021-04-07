# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.Services.as_view(), name="Services"),
path('edit-service/<int:id>', views.EditService.as_view(), name="EditService"),
path('delete-service/<int:id>', views.ServiceDelete.as_view(), name="ServiceDelete"),
path('servicestatus', views.ServiceStatus.as_view(), name="ServiceStatus"),


]