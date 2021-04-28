from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import *
from findsupplier.models import *
from survey.models import *
from custom_app.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from django.template.defaulttags import register
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import base64
from django.core.files.base import ContentFile 

@method_decorator(login_required, name="dispatch")
class ManageCms(generic.TemplateView):
	template_name = 'admin/manage-cms/cms.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:

			get_custom_pages=CustomPage.objects.all().order_by('-id')
			return render(request, self.template_name,{'get_custom_pages':get_custom_pages})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		

@method_decorator(login_required, name="dispatch")
class EditCms(generic.TemplateView):
	template_name = 'admin/manage-cms/edit-cms.html'


	def get(self, request,id,*args, **kwargs):
		if request.user.is_superuser:

			get_page_instance=get_object_or_404(CustomPage,id=id)
			return render(request, self.template_name,{'get_page_instance':get_page_instance})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,id,*args, **kwargs):
		if request.user.is_superuser:
			description=request.POST['description']
			get_page_instance=get_object_or_404(CustomPage,id=id)
			if request.POST["cms_image"] :
						format, imgstr = request.POST["cms_image"].split(
							';base64,')
						ext = format.split('/')[-1]

						file_name = "first." + ext
						data = ContentFile(
							base64.b64decode(imgstr), name=file_name)
						get_page_instance.header_image=data
						get_page_instance.save()	
			if CustomPage.objects.filter(id=id).exists():
				CustomPage.objects.filter(id=id).update(description=description)
				messages.success(request,"Successfully Updated")
			else:
				messages.error(request,"Can't be Updated")
			id=str(id)
			return redirect(BASE_URL+'admin/manage-cms/edit/'+id)
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))