
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

@method_decorator(login_required, name="dispatch")
class ManageProducts(generic.TemplateView):
	template_name = 'admin/manage-products/manage-products.html'


	def get(self, request,*args, **kwargs):
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
		
@method_decorator(login_required, name="dispatch")
class DeleteMultiProducts(generic.TemplateView):
	template_name = 'admin/manage-products/manage-products.html'


	def post(self, request,*args, **kwargs):
		product_array=request.POST.getlist('product_array[]')
		
		for data in product_array:
			product_instance = get_object_or_404(SupplierProduct, id=data)
			
			SupplierProduct.objects.filter(id=product_instance.id).delete()
		
		return JsonResponse({'message': 'Deleted successfully.'})