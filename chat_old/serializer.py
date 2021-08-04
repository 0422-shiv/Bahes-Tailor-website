# Import python package.
from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.files.base import ContentFile
import base64
from PIL import Image
# Import user model form Custom User application.
from .models import ChatSystem


class ChatSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSystem
        fields = ('room','message_text','sender_id','receiver_id','send_datetime','read_status','read_datetime')


