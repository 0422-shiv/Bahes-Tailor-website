from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import *
from services.models import *
from survey.models import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from django.template.defaulttags import register
from datetime import datetime
import base64
from django.core.files.base import ContentFile 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name="dispatch")
class ManageServices(generic.TemplateView):
	template_name = 'admin/manage-services/manage-services.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			from_date=None
			to_date=None
			if 'from_date' in request.GET and 'to_date' in request.GET :
				from_date = request.GET['from_date']
				to_date = request.GET['to_date']
				
				from_date_format = datetime.strptime(from_date,"%m/%d/%Y")
				to_date_format = datetime.strptime(to_date,"%m/%d/%Y")
				
				get_services=TailorSpecification.objects.filter(created_dt__range=[from_date_format, to_date_format])
			else:
				get_services=TailorSpecification.objects.all().order_by('-id')
			return render(request, self.template_name,{'get_services':get_services,'from_date':from_date,'to_date':to_date})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,*args, **kwargs):
		if request.user.is_superuser:
			servicename=request.POST['servicename']
			description=request.POST['description']
			
			servicedata=TailorSpecification(tailor_speci=servicename,description=description,created_dt=datetime.now(),created_by=request.user)
			servicedata.save()
			if request.POST["serviceimg"] :
						format, imgstr = request.POST["serviceimg"].split(
							';base64,')
						ext = format.split('/')[-1]

						file_name = "first." + ext
						data = ContentFile(
							base64.b64decode(imgstr), name=file_name)
						servicedata.img=data
						servicedata.save()
			messages.success(request,"Service Successfully Added")
			return HttpResponseRedirect(reverse('manage_services:ManageServices'))
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))


@method_decorator(login_required, name="dispatch")
class EditService(generic.TemplateView):
	template_name = 'admin/manage-services/edit-services.html'


	def get(self, request, id, *args, **kwargs):
		if request.user.is_superuser:

			service_instance = get_object_or_404(TailorSpecification,id=id)
		   
			return render(request, self.template_name,{'service_instance':service_instance})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))

	def post(self, request, id, *args, **kwargs):
		if request.user.is_superuser:
			service_instance = get_object_or_404(TailorSpecification,id=id)
			servicename=request.POST['servicename']
			description=request.POST['description']
			if request.POST["serviceimg"] :
						format, imgstr = request.POST["serviceimg"].split(
							';base64,')
						ext = format.split('/')[-1]

						file_name = "first." + ext
						data = ContentFile(
							base64.b64decode(imgstr), name=file_name)
						service_instance.img=data
						service_instance.save()
			TailorSpecification.objects.filter(id=id).update(tailor_speci=servicename,description=description)
			messages.success(request,"Service Successfully Updated")
			return HttpResponseRedirect(reverse('manage_services:ManageServices'))
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))

@method_decorator(login_required, name="dispatch")
class ServiceStatus(generic.TemplateView):
	template_name = 'admin/manage-services/manage-services.html'

	def post(self, request, *args, **kwargs):
		if request.user.is_superuser:

			serviceid = request.POST["serviceid"]
			servicestatus = request.POST["servicestatus"]

			if servicestatus == "True":
				status = False
			else:
				status = True
			if TailorSpecification.objects.filter(id=serviceid).exists():
				
				TailorSpecification.objects.filter(id=serviceid).update(status=status)
			return JsonResponse({'message': 'Status Changed successfully.'})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))

@method_decorator(login_required, name="dispatch")
class ServiceDelete(generic.TemplateView):

	def post(self, request, id, *args, **kwargs):
		if request.user.is_superuser:

			service_instance = get_object_or_404(TailorSpecification, id=id)
		   
			TailorSpecification.objects.filter(id=service_instance.id).delete()
			return HttpResponseRedirect(reverse('manage_services:ManageServices'))
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))


@method_decorator(login_required, name="dispatch")
class ChangeAllServiceStatus(generic.TemplateView):
	template_name = 'admin/manage-services/manage-services.html'

	def post(self, request, *args, **kwargs):
		if request.user.is_superuser:

			service_array = request.POST.getlist("service_array[]")
			
			status = request.POST["status"]
			
			if status == "Deactivate":
				changestatus = False
			else:
				changestatus = True
			for data in service_array:
				
				if TailorSpecification.objects.filter(id=data).exists():
					print('in',data)
					TailorSpecification.objects.filter(id=data).update(status=changestatus)
			return JsonResponse({'message': 'Status Changed successfully.'})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))