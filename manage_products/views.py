
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import *
from products.models import *
from survey.models import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from django.template.defaulttags import register
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import os

@method_decorator(login_required, name="dispatch")
class ManageProducts(generic.TemplateView):
	template_name = 'admin/manage-products/manage-products.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			from_date=None
			to_date=None
			if 'from_date' in request.GET and 'to_date' in request.GET :
				from_date = request.GET['from_date']
				to_date = request.GET['to_date']
				
				from_date_format = datetime.strptime(from_date,"%m/%d/%Y")
				to_date_format = datetime.strptime(to_date,"%m/%d/%Y")
				get_products=SupplierProduct.objects.filter(created_dt__range=[from_date_format, to_date_format])
			else:
				get_products=SupplierProduct.objects.all()
			return render(request, self.template_name,{'get_products':get_products,'from_date':from_date,'to_date':to_date})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		
@method_decorator(login_required, name="dispatch")
class DeleteMultiProducts(generic.TemplateView):
	template_name = 'admin/manage-products/manage-products.html'


	def post(self, request,*args, **kwargs):
		product_array=request.POST.getlist('product_array[]')
		
		for data in product_array:
			product_instance = get_object_or_404(SupplierProduct, id=data)
			
			SupplierProduct.objects.filter(id=product_instance.id).delete()
		
		return JsonResponse({'message': 'Deleted successfully.'})
		

@method_decorator(login_required, name="dispatch")
class WashingMethod(generic.TemplateView):
	template_name = 'admin/manage-products/washing-method.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			get_washing_method=Washing_method.objects.all()
			return render(request, self.template_name,{'get_washing_method':get_washing_method})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))



@method_decorator(login_required, name="dispatch")
class AddWashingMethod(generic.TemplateView):
	template_name = 'admin/manage-products/add-washing-method.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			return render(request, self.template_name)
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,*args, **kwargs):		
		washing_obj=Washing_method(name=request.POST['method_name'],image=request.FILES['method_img'],created_by=request.user)
		washing_obj.save()
		messages.success(request,'Successfully Added')
		return HttpResponseRedirect(reverse('manage_products:WashingMethod'))


@method_decorator(login_required, name="dispatch")
class EditWashingMethod(generic.TemplateView):
	template_name = 'admin/manage-products/edit-washing-method.html'
	def get(self, request,id,*args, **kwargs):
		if request.user.is_superuser:
			washing_ins=get_object_or_404(Washing_method,id=id)
			return render(request, self.template_name,{'washing_ins':washing_ins})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,id,*args, **kwargs):
		get_washing_ins=get_object_or_404(Washing_method,id=id)
		Washing_method.objects.filter(id=id).update(name=request.POST['method_name'],created_by=request.user)
		if "method_img" in request.FILES :
			image_path=get_washing_ins.image.path
			if os.path.exists(image_path):
					os.remove(image_path)
					get_washing_ins.image=request.FILES["method_img"]
					get_washing_ins.save()	
		messages.success(request,'Successfully Updated')	
		return HttpResponseRedirect(reverse('manage_products:WashingMethod'))



@method_decorator(login_required, name="dispatch")
class DeleteWashingMethod(generic.TemplateView):
	def post(self, request,id,*args, **kwargs):		
		Washing_method.objects.filter(id=id).delete()
		return HttpResponseRedirect(reverse('manage_products:WashingMethod'))


# -------------------------------------------------------------fabric types methods-------------------------
@method_decorator(login_required, name="dispatch")
class FabricTypes(generic.TemplateView):
	template_name = 'admin/manage-products/fabric-types.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			get_fabric_types=Fabric_type.objects.all()
			return render(request, self.template_name,{'get_fabric_types':get_fabric_types})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))


@method_decorator(login_required, name="dispatch")
class AddFabricTypes(generic.TemplateView):
	template_name = 'admin/manage-products/add-fabric-type.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			return render(request, self.template_name)
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,*args, **kwargs):		
		Fabric_type_obj=Fabric_type(name=request.POST['name'],created_by=request.user)
		Fabric_type_obj.save()
		messages.success(request,'Successfully Added')
		return HttpResponseRedirect(reverse('manage_products:FabricTypes'))



@method_decorator(login_required, name="dispatch")
class EditFabricTypes(generic.TemplateView):
	template_name = 'admin/manage-products/edit-fabric-type.html'
	def get(self, request,id,*args, **kwargs):
		if request.user.is_superuser:
			fabric_type_ins=get_object_or_404(Fabric_type,id=id)
			return render(request, self.template_name,{'fabric_type_ins':fabric_type_ins})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,id,*args, **kwargs):
		Fabric_type.objects.filter(id=id).update(name=request.POST['name'],created_by=request.user)
		messages.success(request,'Successfully Updated')	
		return HttpResponseRedirect(reverse('manage_products:FabricTypes'))


@method_decorator(login_required, name="dispatch")
class DeleteFabricType(generic.TemplateView):
	def post(self, request,id,*args, **kwargs):		
		Fabric_type.objects.filter(id=id).delete()
		return HttpResponseRedirect(reverse('manage_products:FabricTypes'))


# -------------------------------------------------------------Thread types methods-------------------------
@method_decorator(login_required, name="dispatch")
class ThreadTypes(generic.TemplateView):
	template_name = 'admin/manage-products/thread-types.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			get_thread_types=Thread_type.objects.all()
			return render(request, self.template_name,{'get_thread_types':get_thread_types})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))


@method_decorator(login_required, name="dispatch")
class AddThreadTypes(generic.TemplateView):
	template_name = 'admin/manage-products/add-thread-type.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			return render(request, self.template_name)
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,*args, **kwargs):		
		thread_type_obj=Thread_type(name=request.POST['name'],created_by=request.user)
		thread_type_obj.save()
		messages.success(request,'Successfully Added')
		return HttpResponseRedirect(reverse('manage_products:ThreadTypes'))



@method_decorator(login_required, name="dispatch")
class EditThreadTypes(generic.TemplateView):
	template_name = 'admin/manage-products/edit-thread-type.html'
	def get(self, request,id,*args, **kwargs):
		if request.user.is_superuser:
			thread_type_ins=get_object_or_404(Thread_type,id=id)
			return render(request, self.template_name,{'thread_type_ins':thread_type_ins})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,id,*args, **kwargs):
		Thread_type.objects.filter(id=id).update(name=request.POST['name'],created_by=request.user)
		messages.success(request,'Successfully Updated')	
		return HttpResponseRedirect(reverse('manage_products:ThreadTypes'))


@method_decorator(login_required, name="dispatch")
class DeleteThreadType(generic.TemplateView):
	def post(self, request,id,*args, **kwargs):		
		Thread_type.objects.filter(id=id).delete()
		return HttpResponseRedirect(reverse('manage_products:ThreadTypes'))




# -------------------------------------------------------------Buttons types methods-------------------------
@method_decorator(login_required, name="dispatch")
class ButtonTypes(generic.TemplateView):
	template_name = 'admin/manage-products/button-types.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			get_material1_types=Material_type1.objects.all()
			return render(request, self.template_name,{'get_material1_types':get_material1_types})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))


@method_decorator(login_required, name="dispatch")
class AddButtonTypes(generic.TemplateView):
	template_name = 'admin/manage-products/add-button-types.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			return render(request, self.template_name)
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,*args, **kwargs):		
		thread_type_obj=Material_type1(name=request.POST['name'],created_by=request.user)
		thread_type_obj.save()
		messages.success(request,'Successfully Added')
		return HttpResponseRedirect(reverse('manage_products:ButtonTypes'))



@method_decorator(login_required, name="dispatch")
class EditButtonTypes(generic.TemplateView):
	template_name = 'admin/manage-products/edit-button-type.html'
	def get(self, request,id,*args, **kwargs):
		if request.user.is_superuser:
			material1_ins=get_object_or_404(Material_type1,id=id)
			return render(request, self.template_name,{'material1_ins':material1_ins})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,id,*args, **kwargs):
		Material_type1.objects.filter(id=id).update(name=request.POST['name'],created_by=request.user)
		messages.success(request,'Successfully Updated')	
		return HttpResponseRedirect(reverse('manage_products:ButtonTypes'))


@method_decorator(login_required, name="dispatch")
class DeleteButtonType(generic.TemplateView):
	def post(self, request,id,*args, **kwargs):		
		Material_type1.objects.filter(id=id).delete()
		return HttpResponseRedirect(reverse('manage_products:ButtonTypes'))




# -------------------------------------------------------------Elastic,tape,trim types methods-------------------------
@method_decorator(login_required, name="dispatch")
class ElasticTypes(generic.TemplateView):
	template_name = 'admin/manage-products/elastic-types.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			get_material2_types=Material_type2.objects.all()
			return render(request, self.template_name,{'get_material2_types':get_material2_types})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))


@method_decorator(login_required, name="dispatch")
class AddElasticTypes(generic.TemplateView):
	template_name = 'admin/manage-products/add-elastic-types.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			return render(request, self.template_name)
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,*args, **kwargs):		
		elastic_type_obj=Material_type2(name=request.POST['name'],created_by=request.user)
		elastic_type_obj.save()
		messages.success(request,'Successfully Added')
		return HttpResponseRedirect(reverse('manage_products:ElasticTypes'))



@method_decorator(login_required, name="dispatch")
class EditElasticTypes(generic.TemplateView):
	template_name = 'admin/manage-products/edit-elastic-type.html'
	def get(self, request,id,*args, **kwargs):
		if request.user.is_superuser:
			material2_ins=get_object_or_404(Material_type2,id=id)
			return render(request, self.template_name,{'material2_ins':material2_ins})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request,id,*args, **kwargs):
		Material_type2.objects.filter(id=id).update(name=request.POST['name'],created_by=request.user)
		messages.success(request,'Successfully Updated')	
		return HttpResponseRedirect(reverse('manage_products:ElasticTypes'))


@method_decorator(login_required, name="dispatch")
class DeleteElasticType(generic.TemplateView):
	def post(self, request,id,*args, **kwargs):		
		Material_type2.objects.filter(id=id).delete()
		return HttpResponseRedirect(reverse('manage_products:ElasticTypes'))