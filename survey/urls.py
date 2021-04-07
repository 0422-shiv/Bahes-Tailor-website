# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
path('<int:id>', views.Questions.as_view(), name="Questions"),



]