# Import some useful packages.
from django.urls import path
from django.contrib.auth.models import User, auth
from . import views

# Define urls for User Application function.
urlpatterns = [
# path('', views.Chat.as_view(), name="Chat"),
path('chat-user', views.ChatUser.as_view(), name="ChatUser"),
 path('user/room/', views.room,name='room'),
 path('user/messagesubmit/', views.messagesubmit,name='messagesubmit'),
  path('user/messagesubmit/', views.messagesubmit,name='messagesubmit'),
   path('user/get_message_count/<int:id>', views.message_counter,name='message_counter'),
   path('mute_chat-status', views.mute_chat_status,name='mute_chat_status'),
]