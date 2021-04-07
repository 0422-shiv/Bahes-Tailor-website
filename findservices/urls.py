# Import some useful packages.
from django.urls import path
from django.contrib.auth.models import User, auth
from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.FindServices.as_view(), name="FindServices"),


]