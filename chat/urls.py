# Import some useful packages.
from django.urls import path
from django.contrib.auth.models import User, auth
from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.Chat.as_view(), name="Chat"),
 path('user/<int:id>/', views.room,name='room'),
 path('user/messagesubmit/', views.messagesubmit,name='messagesubmit'),
]