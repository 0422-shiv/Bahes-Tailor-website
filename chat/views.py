from django.views import generic
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from account.models import UserProfile
from django.contrib.auth.models import User, auth
from admin_settings.models import System_settings
from django.http import JsonResponse
from chat.models import *
from datetime import datetime
from .serializer import ChatSystemSerializer
from django.db.models import Q
from django.template.defaulttags import register
from django.db.models import Count
from django.template.loader import render_to_string, get_template
import smtplib
import email.message
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from manage_admin_settings.models import *
from bahes.settings import BASE_URL,images_BASE_URL

# Create your views here.

@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class Chat(generic.TemplateView):
	template_name = "chat/chat.html"

	def get(self, request, *args, **kwargs):
		if 'chatbahesroom' in request.GET:
			chatbahesroom=request.GET['chatbahesroom']
		else:
			chatbahesroom=''
		id_of_user=None
		user_name=None
		if 'id' in request.GET:
		
			id_of_user=request.GET['id']
			user_name= get_object_or_404(UserProfile, id=id_of_user)
			
		user_instance = get_object_or_404(User, id=request.user.id)

		userprofile_instance = get_object_or_404(UserProfile,user_id=user_instance)
		
		get_system_settings = System_settings.objects.all()
		# get_chat_customer=UserProfile.objects.all().filter(user_type__type_name='customer')
		# get_chat_supplier=UserProfile.objects.all().filter(user_type__type_name='supplier')
		# get_cha=list(ChatSystem.objects.filter(Q(receiver_id=request.user) | Q(sender_id=request.user)).order_by('-send_datetime'))
		# get_chat_user = list(dict.fromkeys(get_cha))
		# print(get_cha)
		get_chat_list1=list(ChatSystem.objects.filter(Q(receiver_id=request.user) | Q(sender_id=request.user)).values_list('sender_id', flat=True).order_by('-send_datetime'))
		get_chat_list2=list(ChatSystem.objects.filter(Q(receiver_id=request.user) | Q(sender_id=request.user)).values_list('receiver_id', flat=True).order_by('-send_datetime'))
		
		get_merged_list = get_chat_list1+get_chat_list2
		
		get_merged_chat = list(dict.fromkeys(get_merged_list))
		# print(get_merged_chat)
		get_chat_user=User.objects.filter(id__in=get_merged_list)
		get_chat=list(ChatSystem.objects.filter((Q(receiver_id__id__in=get_merged_list) & Q(sender_id=request.user)) | (Q(receiver_id=request.user) & Q(sender_id__id__in=get_merged_list))).order_by('-send_datetime'))
		# print(get_chat)
		
		return render(request, self.template_name,{'get_chat':get_chat,'user_name':user_name,'id_of_user':id_of_user,'get_chat_user':get_chat_user,'chatbahesroom':chatbahesroom,'userprofile': userprofile_instance,'get_system_settings':get_system_settings})


def room(request,id):
	
	userprofile_instance = get_object_or_404(UserProfile,id=id)
	get_id=userprofile_instance.user_id.id

	get_name=userprofile_instance.full_name
	get_status=userprofile_instance.online_status
	
	if ChatSystem.objects.filter(Q(sender_id=userprofile_instance.user_id) & Q(receiver_id=request.user)).exists():
		get_read_status=ChatSystem.objects.filter(Q(sender_id=userprofile_instance.user_id) & Q(receiver_id=request.user))
	
		for data in get_read_status:
			if data.read_status == False:
				ChatSystem.objects.filter(Q(sender_id=userprofile_instance.user_id) & Q(receiver_id=request.user)).update(read_status=True,read_datetime=datetime.now())
	if ChatSystem.objects.filter(((Q(sender_id__id=request.user.id) & Q(receiver_id__id=userprofile_instance.user_id.id)) | (Q(sender_id__id=userprofile_instance.user_id.id) & Q(receiver_id__id=request.user.id)))).exists():
		get_chat=ChatSystem.objects.filter(((Q(sender_id__id=request.user.id) & Q(receiver_id__id=userprofile_instance.user_id.id)) | (Q(sender_id__id=userprofile_instance.user_id.id) & Q(receiver_id__id=request.user.id)))).order_by('id')
		
	else:
		get_chat=ChatSystem.objects.filter((Q(sender_id__id=request.user.id) & Q(receiver_id__id=userprofile_instance.user_id.id))).order_by('id')
	get_data = ChatSystemSerializer(get_chat, many=True)
	chat_data = get_data.data	
	return JsonResponse({'chat_data':chat_data,'get_name':get_name,'get_id':get_id,'get_status':get_status,'id':id})

	# return render(request, 'chat/chatroom.html', {'userprofile_instance':userprofile_instance,'room_name': room_name})

@login_required
def messagesubmit(request):
	
	if request.method == 'POST': 
		
		message_text=request.POST['message']
		sender_id=request.POST['sender']
		sender_instance = get_object_or_404(User, id=sender_id)
		receiver_id=request.POST['reciever']
		receiver_instance = get_object_or_404(User, id=receiver_id)
		messagesubmit=ChatSystem(message_text=message_text,sender_id=sender_instance,receiver_id=receiver_instance,send_datetime=datetime.now())
		messagesubmit.save()
		img=images_BASE_URL+''+sender_instance.userx.image.url
		message_link=BASE_URL+"chat/?chatbahesroom=chatbahesroom&id="+str(sender_instance.userx.id)
		if receiver_instance.userx.online_status == False :
		   
			data_content = {"img":img,
							"sender_name": sender_instance.userx.full_name,
							"message_link":message_link}
			email_content = 'email_template/user-offline.html'

			email_template = get_template(email_content).render(data_content)
			reciver_email = receiver_instance.email

			Subject = sender_instance.userx.full_name +' just messaged you'
			if Email_Setting.objects.filter(status=True).exists():
				email_data = Email_Setting.objects.filter(status=True)
				for data in email_data:
					EMAIL_HOST = data.smtp_host
					EMAIL_PORT = data.smtp_port
					EMAIL_HOST_USER = data.smtp_username
					EMAIL_HOST_PASSWORD = data.smtp_password
			email_msg = EmailMessage(Subject, email_template, EMAIL_HOST_USER, [reciver_email],
									 reply_to=[EMAIL_HOST_USER])
			email_msg.content_subtype = 'html'
			email_msg.send(fail_silently=False)
		
		
	return JsonResponse({'get_name':'submitted'})




@login_required
def message_counter(request,id):
	

	get_message_counter = 0	

	if ChatSystem.objects.filter(Q(sender_id__userx__id=id) & Q(receiver_id=request.user)).exists():
				get_unread_status=ChatSystem.objects.filter(Q(sender_id__userx__id=id) & Q(receiver_id=request.user))
				get_unread_message_list=[]
				for data in get_unread_status:
					
					if data.read_status == False:
						
						get_unread_message_list.append(data.read_status)
						
					
				get_message_counter=(len(get_unread_message_list))	
			
	
	return JsonResponse({'get_message_counter':get_message_counter})


@register.filter(name='total_message_counter')
def total_message_counter(id):
	get_total_message_counter = 0
	if ChatSystem.objects.filter(receiver_id=id).exists():
			get_read_status=ChatSystem.objects.filter(receiver_id=id)
			
			get_unread_message_list=[]
			for data in get_read_status:
				if data.read_status == False:
					get_unread_message_list.append(data.read_status)
					
					
			get_total_message_counter=(len(get_unread_message_list))	
	return get_total_message_counter


@register.filter(name='get_audio_url')
def get_audio_url(data,currentuser):
	
	get_audio_url = None
	if UserProfile.objects.filter(user_id__id=currentuser.id).exists():
		get_mute_status=get_object_or_404(UserProfile,user_id__id=currentuser.id)
		if get_mute_status.chat_mute_status == True:
			get_audio_obj=MuteChat.objects.all()
			if 'sender_audio' == data:
					
					for data in get_audio_obj:
						get_audio_url=data.sending_mess_sound
					
			if 'receiver_audio' == data:
					
					for data in get_audio_obj:
						get_audio_url=data.receiving_mess_sound
					
				
	return get_audio_url


@login_required
def mute_chat_status(request):
	
	
	if request.method == 'POST': 
		userid=request.POST['userid']
		chat_mute_status=request.POST['chat_mute_status']
		if chat_mute_status == "True":
			status = False
		else:
			status = True
		if UserProfile.objects.filter(id=userid).exists():
			   
			UserProfile.objects.filter(id=userid).update(chat_mute_status=status)
		return JsonResponse({'message': 'Status Changed successfully.'})
