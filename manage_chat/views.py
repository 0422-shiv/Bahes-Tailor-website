from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from chat.models import *
from django.http import JsonResponse
from chat.serializer import ChatSystemSerializer
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

@method_decorator(login_required, name="dispatch")
class ManageChat(generic.TemplateView):
	template_name = 'admin/chat/chat.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			get_chat = ChatSystem.objects.distinct('sender_id','receiver_id')
		
			return render(request, self.template_name,{'get_chat':get_chat})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))





@login_required
def Get_Chat_History(request):
	if request.user.is_superuser:
		senderid=request.GET['senderid']
		receiverid=request.GET['receiverid']
		
		if ChatSystem.objects.filter(((Q(sender_id__id=senderid) & Q(receiver_id__id=receiverid)) | (Q(sender_id__id=receiverid) & Q(receiver_id__id=senderid)))).exists():
			get_chat=ChatSystem.objects.filter(((Q(sender_id__id=senderid) & Q(receiver_id__id=receiverid)) | (Q(sender_id__id=receiverid) & Q(receiver_id__id=senderid)))).order_by('id')
			
		else:
			get_chat=ChatSystem.objects.filter((Q(sender_id__id=senderid) & Q(receiver_id__id=receiverid))).order_by('id')
		# print(get_chat)
		get_data = ChatSystemSerializer(get_chat, many=True)
		chat_data = get_data.data	
		return JsonResponse({'chat_data':chat_data,'senderid':senderid,'receiverid':receiverid})
	else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))