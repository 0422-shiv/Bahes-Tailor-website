# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [

path('', views.ManageChat.as_view(), name="ManageChat"),
path('chat-history/', views.Get_Chat_History,name='Get_Chat_History'),



]