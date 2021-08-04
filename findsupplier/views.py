from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from admin_settings.models import System_settings
from services.models import *
from products.models import *
from account.models import *
from .models import *
from survey.models import *
from django.db.models import Count,Max
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
import smtplib
import email.message
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from manage_admin_settings.models import *
import requests 
import json
from bahes.settings import BASE_URL




###########Send Payment##########
baseURL='https://api.myfatoorah.com'
token = 'htmKx0gxzlblycd_kTt2AHI4xhodwEQ-Ytho58gMnxxMLaOiOr7TaH_fqwmE1zdp4X5np68gyvdOvLcUi2wCldqb1l1yubkKcJC_5AGYmki9KrLZgaHs6gFyPMyU2LIJl2KJQvNzDfvT76iQeEbEV9taGEoSZpxFgrp9NokClY7Kw0pyjG33WJs5sVxqvNDju2R3Sn6itvwh45dbVs9ACXpANBK4O0rzUDZJScWIyO9RVaZouWOupSj7wTWSAdNzArKLtJvGjl5QrV4OPkjpuz4cD3FO-exUw4fJ2DqPnmOW9wduc5AXCzXsteRnCfl6LBhxP7_Sb8tc0OmJwPGxHHFZ1pbNSEvWf5tYw_JT7X4S4BwKiuKLpGrU8Rzgn41pBSNS3L0TYVy0W9TEqSUaQO4B1jSDtOgxFMs11BY-VYrT9rEa4xGvci0gss3y8id5cUAapiPwujOiV1M7nnlFyXLleEfc3v_z0jeTKpasTbZTLO8MvxsSCQ4itxJ6tds8HegoR4cdqoimk8xryy6HokGKgoaEeQfO17yeS7TH8ps3iGiozQz1Rhsret1ASwZzzqBrxHv9SVzmHMO27EjBXbs1yoviOjc376ygByP0b16fTx6uvqCxfmKZE4vE9C86rFfOZb5NVRrUY3En2bLAsvw6eVQl6HJhT-6HwBscmQ-IP4L_' #token value to be placed here
url = baseURL + "/v2/SendPayment"

	# test payment gateway url and token
# baseURL = "https://apitest.myfatoorah.com"  
# token='rLtt6JWvbUHDDhsZnfpAhpYk4dxYDQkbcPTyGaKp2TYqQgG7FGZ5Th_WD53Oq8Ebz6A53njUoo1w3pjU1D4vs_ZMqFiz_j0urb_BH9Oq9VZoKFoJEDAbRZepGcQanImyYrry7Kt6MnMdgfG5jn4HngWoRdKduNNyP4kzcp3mRv7x00ahkm9LAK7ZRieg7k1PDAnBIOG3EyVSJ5kK4WLMvYr7sCwHbHcu4A5WwelxYK0GMJy37bNAarSJDFQsJ2ZvJjvMDmfWwDVFEVe_5tOomfVNt6bOg9mexbGjMrnHBnKnZR1vQbBtQieDlQepzTZMuQrSuKn-t5XZM7V6fCW7oP-uXGX-sMOajeX65JOf6XVpk29DP6ro8WTAflCDANC193yof8-f5_EYY-3hXhJj7RBXmizDpneEQDSaSz5sFk0sV5qPcARJ9zGG73vuGFyenjPPmtDtXtpx35A-BVcOSBYVIWe9kndG3nclfefjKEuZ3m4jL9Gg1h2JBvmXSMYiZtp9MR5I6pvbvylU_PP5xJFSjVTIz7IQSjcVGO41npnwIxRXNRxFOdIUHn0tjQ-7LwvEcTXyPsHXcMD8WtgBh-wxR8aKX7WPSsT1O8d8reb2aR7K3rkV3K82K_0OgawImEpwSvp9MNKynEAJQS6ZHe_J_l77652xwPNxMRTMASk1ZsJL'
# url = baseURL + "/v2/SendPayment"

# Create your views here.
class FindSupplier(generic.TemplateView):
	template_name = "findsupplier/find-supplier.html"

	def get(self, request, *args, **kwargs):
		
		get_system_settings = System_settings.objects.all()
		get_services=TailorSpecification.objects.filter(status=True)
		get_tailor_services=TailorSpecification.objects.filter(status=True)
		get_products=Product_subcategory.objects.all()
		q_list=['Latest','By Name','Oldest']
		get_fabric_product=get_object_or_404(Product_category,slug='fabrics')
		# filters = None
		# if 'service' in self.request.GET:
		# 	filters = filters & Q(TailorSpecification__tailor_speci__in = self.request.GET.getlist('service'))
		# 	print(filters)
		if ('service' in request.GET and 'product' in request.GET) and 'sort-by' in request.GET:
			q_service= self.request.GET.getlist('service')
			q_product = self.request.GET.getlist('product')
			# print('3')
			get_service_user_list=list(SupplierServices.objects.values_list('user_id', flat=True).filter(tailor_speci_id__tailor_speci__in=q_service).filter(status=True))
			get_product_user_list=list(SupplierProduct.objects.values_list('user_id', flat=True).filter(Q(Product_subcategory__subcategory_name__in=q_product) | Q(product_category__category_name__in=q_product)).filter(status=True))
			get_filter_supplier = TailorSpecification.objects.filter(tailor_speci__in=q_service).filter(status=True)
			get_filter_products_subcat=Product_subcategory.objects.filter(subcategory_name__in=q_product)
			get_filter_fabric_product=Product_category.objects.filter(category_name__in=q_product)
			
			list1_as_set = set(get_service_user_list)
			intersection = list1_as_set.intersection(get_product_user_list)

			intersection_as_list = list(intersection)
			q_sort_by=''
			if 'sort-by' in request.GET:
				q_sort_by = self.request.GET['sort-by']
				if q_sort_by == 'Latest':
					get_supp=SupplierServices.objects.filter(user_id__in=intersection_as_list).filter(tailor_speci_id__tailor_speci__in=q_service).filter(status=True).order_by('-user_id').distinct('user_id')

				elif q_sort_by == 'By Name':
					get_supp=SupplierServices.objects.filter(user_id__in=intersection_as_list).filter(tailor_speci_id__tailor_speci__in=q_service).filter(status=True).order_by('user_id__userx__full_name').distinct('user_id__userx__full_name')

				elif q_sort_by == 'Oldest':
					get_supp=SupplierServices.objects.filter(user_id__in=intersection_as_list).filter(tailor_speci_id__tailor_speci__in=q_service).filter(status=True).order_by('user_id').distinct('user_id')

			else :
				get_supp=SupplierServices.objects.filter(user_id__in=intersection_as_list).filter(tailor_speci_id__tailor_speci__in=q_service).filter(status=True) 
			page = request.GET.get('page', 1)
			paginator = Paginator(get_supp, 9) 
			
		
			try:
				get_supplier = paginator.page(page)
			except PageNotAnInteger:
				get_supplier = paginator.page(1)
			except EmptyPage:
					
				get_supplier = paginator.page(paginator.num_pages)
			return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'q_list':q_list,'q_sort_by':q_sort_by,'get_filter_fabric_product':get_filter_fabric_product,'get_filter_products_subcat':get_filter_products_subcat,'get_filter_supplier':get_filter_supplier,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_supplier':get_supplier,'get_services':get_services,'get_system_settings':get_system_settings})
		elif 'service' in request.GET and 'product' in request.GET:
			# print('2')
			q_service= self.request.GET.getlist('service')
			q_product = self.request.GET.getlist('product')
			get_service_user_list=list(SupplierServices.objects.values_list('user_id', flat=True).filter(tailor_speci_id__tailor_speci__in=q_service).filter(status=True))
			get_product_user_list=list(SupplierProduct.objects.values_list('user_id', flat=True).filter(Q(Product_subcategory__subcategory_name__in=q_product) | Q(product_category__category_name__in=q_product)).filter(status=True))
			get_filter_supplier = TailorSpecification.objects.filter(tailor_speci__in=q_service).filter(status=True)
			get_filter_products_subcat=Product_subcategory.objects.filter(subcategory_name__in=q_product)
			get_filter_fabric_product=Product_category.objects.filter(category_name__in=q_product)
			
			list1_as_set = set(get_service_user_list)
			intersection = list1_as_set.intersection(get_product_user_list)

			intersection_as_list = list(intersection)

			
			get_supp=SupplierServices.objects.filter(user_id__in=intersection_as_list).filter(tailor_speci_id__tailor_speci__in=q_service).filter(status=True).distinct('user_id') 
			page = request.GET.get('page', 1)
			paginator = Paginator(get_supp, 9) 
			
		
			try:
				get_supplier = paginator.page(page)
			except PageNotAnInteger:
				get_supplier = paginator.page(1)
			except EmptyPage:
					
				get_supplier = paginator.page(paginator.num_pages)
			return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'q_list':q_list,'get_filter_fabric_product':get_filter_fabric_product,'get_filter_products_subcat':get_filter_products_subcat,'get_filter_supplier':get_filter_supplier,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_supplier':get_supplier,'get_services':get_services,'get_system_settings':get_system_settings})
		
		
		elif 'service' in request.GET and 'sort-by' in request.GET:
			q = self.request.GET.getlist('service')
			get_filter_supplier = TailorSpecification.objects.filter(tailor_speci__in=q).filter(status=True)
			print('service sort')
			q_sort_by = self.request.GET['sort-by']
			if q_sort_by == 'Latest':
					get_supp=SupplierServices.objects.filter(tailor_speci_id__tailor_speci__in=q).filter(status=True).order_by('-user_id').distinct('user_id')
			elif q_sort_by == 'By Name':
					get_supp=SupplierServices.objects.filter(tailor_speci_id__tailor_speci__in=q).filter(status=True).order_by('user_id__userx__full_name').distinct('user_id__userx__full_name')
			elif q_sort_by == 'Oldest':
					get_supp=SupplierServices.objects.filter(tailor_speci_id__tailor_speci__in=q).filter(status=True).order_by('user_id').distinct('user_id')
			else :
					get_supp=SupplierServices.objects.filter(tailor_speci_id__tailor_speci__in=q).filter(status=True)
			page = request.GET.get('page', 1)
			paginator = Paginator(get_supp, 9) 
			
		
			try:
				get_supplier = paginator.page(page)
			except PageNotAnInteger:
				get_supplier = paginator.page(1)
			except EmptyPage:
					
				get_supplier = paginator.page(paginator.num_pages)
			return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'q_list':q_list,'q_sort_by':q_sort_by,'get_filter_supplier':get_filter_supplier,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_supplier':get_supplier,'get_services':get_services,'get_system_settings':get_system_settings})
		
		elif 'service' in request.GET :
			q = self.request.GET.getlist('service')
			get_filter_supplier = TailorSpecification.objects.filter(tailor_speci__in=q).filter(status=True)
			# print('service')
			get_supp=SupplierServices.objects.filter(tailor_speci_id__tailor_speci__in=q).filter(status=True).distinct('user_id')
			page = request.GET.get('page', 1)
			paginator = Paginator(get_supp, 9) 
			
		
			try:
				get_supplier = paginator.page(page)
			except PageNotAnInteger:
				get_supplier = paginator.page(1)
			except EmptyPage:
					
				get_supplier = paginator.page(paginator.num_pages)
			return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'q_list':q_list,'get_filter_supplier':get_filter_supplier,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_supplier':get_supplier,'get_services':get_services,'get_system_settings':get_system_settings})

		elif 'product' in request.GET and 'sort-by' in request.GET:
			q = self.request.GET.getlist('product')
			# get_product_user=SupplierProduct.objects.values_list('user_id', flat=True).order_by().annotate(max_id=Max('id'), count_id=Count('id')).filter(count_id__gt=1)
			q_sort_by = self.request.GET['sort-by']
			# print('product sort')
			get_product_user_list=SupplierProduct.objects.values_list('user_id', flat=True).filter(status=True).filter(Q(Product_subcategory__subcategory_name__in=q) | Q(product_category__category_name__in=q))
			if q_sort_by == 'Latest':
				get_supp=SupplierServices.objects.filter(user_id__in=get_product_user_list).order_by('-user_id').distinct('user_id')

			elif q_sort_by == 'By Name':
				get_supp=SupplierServices.objects.filter(user_id__in=get_product_user_list).order_by('user_id__userx__full_name').distinct('user_id__userx__full_name')

			elif q_sort_by == 'Oldest':
				get_supp=SupplierServices.objects.filter(user_id__in=get_product_user_list).order_by('-user_id').distinct('user_id')
			else:
				get_supp=SupplierServices.objects.filter(user_id__in=get_product_user_list).distinct('user_id')
			get_filter_products_subcat=Product_subcategory.objects.filter(subcategory_name__in=q)
			get_filter_fabric_product=Product_category.objects.filter(category_name__in=q)
			page = request.GET.get('page', 1)
			paginator = Paginator(get_supp, 9) 
			
		
			try:
				get_supplier = paginator.page(page)
			except PageNotAnInteger:
				get_supplier = paginator.page(1)
			except EmptyPage:
					
				get_supplier = paginator.page(paginator.num_pages)
		
			return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'q_list':q_list,'q_sort_by':q_sort_by,'get_filter_fabric_product':get_filter_fabric_product,'get_filter_products_subcat':get_filter_products_subcat,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_supplier':get_supplier,'get_services':get_services,'get_system_settings':get_system_settings})

		elif 'product' in request.GET:
			q = self.request.GET.getlist('product')
			# get_product_user=SupplierProduct.objects.values_list('user_id', flat=True).order_by().annotate(max_id=Max('id'), count_id=Count('id')).filter(count_id__gt=1)
			# print('product')
			get_product_user_list=SupplierProduct.objects.values_list('user_id', flat=True).filter(Q(Product_subcategory__subcategory_name__in=q) | Q(product_category__category_name__in=q)).filter(status=True)
			get_supp=SupplierServices.objects.filter(user_id__in=get_product_user_list).distinct('user_id')
			get_filter_products_subcat=Product_subcategory.objects.filter(subcategory_name__in=q)
			get_filter_fabric_product=Product_category.objects.filter(category_name__in=q)
			page = request.GET.get('page', 1)
			paginator = Paginator(get_supp, 9) 
			
		
			try:
				get_supplier = paginator.page(page)
			except PageNotAnInteger:
				get_supplier = paginator.page(1)
			except EmptyPage:
					
				get_supplier = paginator.page(paginator.num_pages)
		
			return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'q_list':q_list,'get_filter_fabric_product':get_filter_fabric_product,'get_filter_products_subcat':get_filter_products_subcat,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_supplier':get_supplier,'get_services':get_services,'get_system_settings':get_system_settings})

		elif 'sort-by' in request.GET:
			q_sort_by = self.request.GET['sort-by']
			
			# print('sort-by')
			if q_sort_by == 'Latest':
				get_supp=SupplierServices.objects.filter(status=True).order_by('-user_id').distinct('user_id')
			if q_sort_by == 'By Name':
				get_supp=SupplierServices.objects.filter(status=True).order_by('user_id__userx__full_name').distinct('user_id__userx__full_name')
			if q_sort_by == 'Oldest':
				get_supp=SupplierServices.objects.filter(status=True).order_by('user_id').distinct('user_id')
			page = request.GET.get('page', 1)
			paginator = Paginator(get_supp, 9) 
			
		
			try:
				get_supplier = paginator.page(page)
			except PageNotAnInteger:
				get_supplier = paginator.page(1)
			except EmptyPage:
					
				get_supplier = paginator.page(paginator.num_pages)
			return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'q_list':q_list,'q_sort_by':q_sort_by,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_supplier':get_supplier,'get_services':get_services,'get_system_settings':get_system_settings})


		else:
			get_supp=SupplierServices.objects.filter(status=True).distinct('user_id')
			page = request.GET.get('page', 1)
			paginator = Paginator(get_supp, 9) 
			
		
			try:
				get_supplier = paginator.page(page)
			except PageNotAnInteger:
				get_supplier = paginator.page(1)
			except EmptyPage:
					
				get_supplier = paginator.page(paginator.num_pages)
			return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'q_list':q_list,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_supplier':get_supplier,'get_services':get_services,'get_system_settings':get_system_settings})

# @method_decorator(login_required(login_url='/account/login'), name="dispatch")		
class Payment(generic.TemplateView):
	
	def get(self, request,*args, **kwargs):
		if request.user.is_authenticated:

			get_registration_fee=RegistraionFees.objects.all()
			if UserProfile.objects.filter(user_id=request.user).exists():
						userprofile_instance = get_object_or_404(UserProfile,user_id=request.user)
						if not userprofile_instance.user_type == None :
										if not UserAnswerTable.objects.filter(user=request.user).exists():
												return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
										elif UserAnswerTable.objects.filter(user=request.user).exists():
												if request.user.userx.user_type.type_name == 'supplier':
														if not (UserAnswerTable.objects.filter(user=request.user).count()) == 4:
																UserAnswerTable.objects.filter(user=request.user).delete()
																return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
														else:
															return render(request,"findsupplier/customer-payment.html",{'get_registration_fee':get_registration_fee})
												elif request.user.userx.user_type.type_name == 'customer':
														if not (UserAnswerTable.objects.filter(user=request.user).count()) == 2:
																UserAnswerTable.objects.filter(user=request.user).delete()
																return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
														else:
															return render(request,"findsupplier/customer-payment.html",{'get_registration_fee':get_registration_fee})
													
						else:
								return HttpResponse('usertype')
			else:
					return HttpResponse('usertype')
		else:
			return HttpResponse('login')
			# return render(request,"account/login.html")


		
			


@method_decorator(login_required(login_url='/account/login'), name="dispatch")			
class SendPayment(generic.TemplateView):
	
	def get(self, request,*args, **kwargs):
		if BahesPayment.objects.filter(user_id=request.user).filter(payment_status=True).exists():
			pass
		else:
			amount=request.GET['amount']
			currency_type=request.GET['currency_type']
			user_instance=get_object_or_404(UserProfile,user_id=request.user)
			name=user_instance.full_name
			if not (user_instance.tel_code is None):
				tel_code='+'+str(user_instance.tel_code)
			else:
				tel_code=''
			if not (user_instance.phone is None):
				phone=str(user_instance.phone)
			else:
				phone=''
			if not (user_instance.user_id.email is None):
				email=user_instance.user_id.email
			else:
				email=''
			id=user_instance.user_id.id
			call_back_url=BASE_URL+'find-supplier/customer-payment-done/?amount='+amount+'&currency_type='+currency_type
			body= {'NotificationOption': 'ALL',
				     'CustomerName': name,
				     'DisplayCurrencyIso': currency_type,
				     'MobileCountryCode': tel_code,
				     'CustomerMobile': phone,
				     'CustomerEmail':email,
				     'InvoiceValue': amount,
				     'CallBackUrl': call_back_url,
				     'ErrorUrl': call_back_url,
				     'Language': 'en',
				     'CustomerReference': id,
				     'CustomerCivilId': 12345678,
				     'UserDefinedField': 'Custom field',
				     'ExpireDate': '',
				     'CustomerAddress': 
				      { 'Block': '',
				        'Street': '',
				        'HouseBuildingNo': '',
				        'Address': '',
				        'AddressInstructions': '' },
				     'InvoiceItems': [ { 'ItemName': 'Business Owner', 'Quantity': 1, 'UnitPrice': amount } ] }
		
		
			headers = {'Content-Type': "application/json", 'Authorization': "Bearer " + token}
			pay=str(body)
			response = requests.request("POST", url, data=pay, headers=headers)
			data_dict = json.loads(response.text)
			
			data_url = data_dict["Data"]
	
			payment_url=data_url["InvoiceURL"]
			# return HttpResponse(payment_url)
			# return HttpResponse({'amount':amount,'currency_type':currency_type,'name':name,'tel_code':tel_code,'phone':phone,'email':email,'data_dict':data_dict})

			return JsonResponse({'url':payment_url})  
		
	
			

@method_decorator(login_required(login_url='/account/login'), name="dispatch")			
class PaymentDone(generic.TemplateView):
	
	def get(self, request,*args, **kwargs):
		if 'paymentId' in request.GET:
			paymentId=request.GET['paymentId']
			amount=request.GET['amount']
			currency_type=request.GET['currency_type']
			savepayment=BahesPayment(user_id=request.user,transaction_id=paymentId,amount=amount,currency_type=currency_type,payment_status=True,payment_date=datetime.now())
			savepayment.save()
			user_instance=get_object_or_404(UserProfile,user_id__id=request.user.id)
			
			data_content = {"username": user_instance.full_name,}
			email_content = 'email_template/payment.html'

			email_template = get_template(email_content).render(data_content)
			reciver_email = user_instance.user_id.email

			Subject = 'Thank you for your payment'
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
		return redirect(BASE_URL+'?paymentdone=paymentdone')

	
		
class SupplierView(generic.TemplateView):
	template_name = "findsupplier/supplier-view.html"

	def get(self, request,id, *args, **kwargs):
		get_payment=None
		if request.user.is_authenticated:
			if BahesPayment.objects.filter(user_id=request.user).exists():
				get_payment=get_object_or_404(BahesPayment,user_id=request.user)
		get_profile=get_object_or_404(UserProfile,user_id__id=id)
		get_system_settings = System_settings.objects.all()
		get_tailor_services=TailorSpecification.objects.filter(status=True)
		get_services=SupplierServices.objects.filter(user_id__id=id).filter(status='True')
		get_product=SupplierProduct.objects.filter(user_id__id=id).filter(status='True')
		return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'get_payment':get_payment,'get_profile':get_profile,'get_product':get_product,'get_services':get_services,'get_system_settings':get_system_settings})
		

