from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import *
from findsupplier.models import *
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse

from bahes.settings import BASE_URL
from django.template.defaulttags import register
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name="dispatch")
class ManageCost(generic.TemplateView):
	template_name = 'admin/manage-payments/manage-cost.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:

			get_registration_fee=RegistraionFees.objects.all()
			return render(request, self.template_name,{'get_registration_fee':get_registration_fee})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))


@method_decorator(login_required, name="dispatch")
class UpdateManageCost(generic.TemplateView):
	template_name = 'admin/manage-payments/edit-manage-cost.html'


	def get(self, request,id,*args, **kwargs):
		if request.user.is_superuser:
	
			get_registration_fee_instance= get_object_or_404(RegistraionFees , id=id )
			return render(request, self.template_name,{'get_registration_fee_instance':get_registration_fee_instance})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))

	def post(self, request,id,*args, **kwargs):
		if request.user.is_superuser:
	
			amount=request.POST['amount']
			content=request.POST['content']
			currency_type=request.POST['currency_type']
			RegistraionFees.objects.filter(id=id).update(amount= amount,content=content,currency_type=currency_type)
			messages.success(request,"One Time Registraion Fee Successfully Updated")
			return HttpResponseRedirect(reverse('manage_payments:ManageCost'))
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		


@method_decorator(login_required, name="dispatch")
class ManageOrder(generic.TemplateView):
	template_name = 'admin/manage-payments/manage-order.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			from_date=None
			to_date=None
			if 'from_date' in request.GET and 'to_date' in request.GET :
				from_date = request.GET['from_date']
				to_date = request.GET['to_date']
				
				from_date_format = datetime.strptime(from_date,"%m/%d/%Y")
				to_date_format = datetime.strptime(to_date,"%m/%d/%Y")
				get_user_payements=BahesPayment.objects.filter(payment_date__range=[from_date_format, to_date_format]).exclude(user_id__is_superuser=True)
			else:
				get_user_payements = BahesPayment.objects.exclude(user_id__is_superuser=True).order_by('-id')
			return render(request, self.template_name,{'get_user_payements':get_user_payements,'from_date':from_date,'to_date':to_date})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))