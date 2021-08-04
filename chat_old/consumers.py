import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from account.models import *

class ChatConsumer(WebsocketConsumer):
    print("connected")
    def connect(self):
        print("connected")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        user = self.scope['user']
      
        self.update_user_status(user, 'True')
        # print(self.)
        # print(self.room_group_name,self.room_name )
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name

        )

        self.accept()

    def disconnect(self, close_code):
        print("disconnected")
        # Leave room group
        user = self.scope['user']
        self.update_user_status(user, 'False')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("receive")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message,text_data_json)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


    # @database_sync_to_async
    def update_user_status(self, user, status):
       
        return UserProfile.objects.filter(user_id__id=user.id).update(online_status=status)