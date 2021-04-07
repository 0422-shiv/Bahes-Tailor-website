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
# Create your views here.

@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class Chat(generic.TemplateView):
	template_name = "chat/chat.html"

	def get(self, request, *args, **kwargs):
		chatbahesroom=request.GET['chatbahesroom']
		id_of_user=None
		if 'id' in request.GET:
		
			id_of_user=request.GET['id']
			
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
		
		return render(request, self.template_name,{'get_chat':get_chat,'id_of_user':id_of_user,'get_chat_user':get_chat_user,'chatbahesroom':chatbahesroom,'userprofile': userprofile_instance,'get_system_settings':get_system_settings})


def room(request,id):
	
	userprofile_instance = get_object_or_404(UserProfile,id=id)
	get_id=userprofile_instance.user_id.id
	get_name=userprofile_instance.full_name
	get_status=userprofile_instance.online_status
	# .filter(Q(sender_id=data.user_id) & Q(receiver_id=id))
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
	return JsonResponse({'chat_data':chat_data,'get_name':get_name,'get_id':get_id,'get_status':get_status})

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
	return JsonResponse({'get_name':'submitted'})




@register.filter(name='message_counter')
def message_counter(data,id):
	get_message_counter = 0
	
	if ChatSystem.objects.filter(Q(sender_id=data) & Q(receiver_id=id)).exists():
			get_unread_status=ChatSystem.objects.filter(Q(sender_id=data) & Q(receiver_id=id))
			
			get_unread_message_list=[]
			for data in get_unread_status:
				
				if data.read_status == False:
					
					get_unread_message_list.append(data.read_status)
					
					
			get_message_counter=(len(get_unread_message_list))	
			
	return get_message_counter



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



@register.filter(name='show_last_chat_user')
def show_last_chat_user(data):
	get_user = 0
	print("===========")
	print(data)
	print("===========")
	# if ChatSystem.objects.filter((Q(receiver_id__id=data) & Q(sender_id=id)) | (Q(receiver_id=id) & Q(sender_id__id=data))).exists():
	# 		get_user=ChatSystem.objects.filter((Q(receiver_id__id=data) & Q(sender_id=request.user)) | (Q(receiver_id=request.user) & Q(sender_id__id=data)))
	# 		print(get_user)

			
				
	return get_user