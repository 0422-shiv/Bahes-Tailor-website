from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from admin_settings.models import System_settings
from services.models import *
from products.models import *
from account.models import *
from .models import *
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
			return render(request,"findsupplier/customer-payment.html",{'get_registration_fee':get_registration_fee})
		else:
			return HttpResponse('login')
			# return render(request,"account/login.html")


	  
	   		

@method_decorator(login_required(login_url='/account/login'), name="dispatch")			
class PaymentDone(generic.TemplateView):
	
	def get(self, request,*args, **kwargs):
		if BahesPayment.objects.filter(user_id=request.user).exists():
			pass
		else:
			amount=request.GET['amount']
			savepayment=BahesPayment(user_id=request.user,amount=amount,payment_status=True,payment_date=datetime.now())
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
		return JsonResponse({'message':'Payment Successfully Done'})  
		

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
	  
	   