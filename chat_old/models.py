from django.db import models
from django.contrib.auth.models import User
import django
class Room(models.Model):
	
	label = models.SlugField(unique=True,null=True, blank=True)
	def __str__(self):
		return str(self.label)

class ChatSystem(models.Model):
	room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE,null=True, blank=True)
	message_text=models.TextField( null=True, blank=True)
	sender_id = models.ForeignKey(User, related_name='sender_id', on_delete=models.CASCADE)
	receiver_id = models.ForeignKey(User, related_name='receiver_id', on_delete=models.CASCADE)
	send_datetime = models.DateTimeField(default=django.utils.timezone.now)
	read_status=models.BooleanField(default=False)
	read_datetime=models.DateTimeField(null=True, blank=True)


	def __str__(self):
		return str(self.sender_id)


class MuteChat(models.Model):
	
	receiving_mess_sound=models.URLField(blank=True, null=True) 
	sending_mess_sound= models.URLField(blank=True, null=True) 
	
	