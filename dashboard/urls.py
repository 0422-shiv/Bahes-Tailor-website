# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
    path('', views.Dashboard.as_view(), name="Dashboard"),
    path('profile/', views.EditProfile.as_view(), name="EditProfile"),
    path('update-password/', views.Updatepassword.as_view(), name="Updatepassword"),
    path('profile-change/', views.ProfileChange, name="profilechange"),
    path('onlinestatus/', views.OnlineStatus, name="OnlineStatus"),

]