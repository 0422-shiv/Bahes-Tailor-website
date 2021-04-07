# Import some useful packages.
from django.urls import path
from django.contrib.auth.models import User, auth
from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.FindProducts.as_view(), name="FindProducts"),
path('detail/<int:id>', views.ProductDetail.as_view(), name="ProductDetail"),

]