from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import *
from findsupplier.models import *
from survey.models import *
from services.models import *
from services.forms import *
from products.models import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from django.template.defaulttags import register
import simplejson as json
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name="dispatch")
class ManageCustomer(generic.TemplateView):
	template_name = 'admin/manage-member/manage-customer.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			from_date=None
			to_date=None
			if 'from_date' in request.GET and 'to_date' in request.GET :
				from_date = request.GET['from_date']
				to_date = request.GET['to_date']
				
				from_date_format = datetime.strptime(from_date,"%m/%d/%Y")
				to_date_format = datetime.strptime(to_date,"%m/%d/%Y")
				get_customer_user=UserProfile.objects.filter(created_date__range=[from_date_format, to_date_format]).filter(user_type__type_name='customer').order_by('-id')
			else:

				get_customer_user=UserProfile.objects.filter(user_type__type_name='customer').order_by('-id')
			# get_customer_payment=BahesPayment.objects.all().filter(user_id__userx__user_type__type_name='customer').order_by('-id')
			
			
			return render(request, self.template_name,{'get_customer_user':get_customer_user,'from_date':from_date,'to_date':to_date})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		



@register.filter(name='answer_status')
def answer_status(data):
	get_answer_status = 'No'
	
	if UserAnswerTable.objects.filter(user=data.user_id).exists():
		get_answer_status='Yes'
	return get_answer_status



@register.filter(name='paid_status')
def paid_status(data):
	
	get_paid_status = 'Unpaid'
	if BahesPayment.objects.filter(user_id=data.user_id).filter(payment_status=True).exists():
		get_paid_status='Paid'
	
	return get_paid_status


@method_decorator(login_required, name="dispatch")
class ManageSupplier(generic.TemplateView):
	template_name = 'admin/manage-member/manage-supplier.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			from_date=None
			to_date=None
			if 'from_date' in request.GET and 'to_date' in request.GET :
				from_date = request.GET['from_date']
				to_date = request.GET['to_date']
				
				from_date_format = datetime.strptime(from_date,"%m/%d/%Y")
				to_date_format = datetime.strptime(to_date,"%m/%d/%Y")
				get_supplier_user=UserProfile.objects.filter(created_date__range=[from_date_format, to_date_format]).filter(user_type__type_name='supplier').order_by('-id')

			else:
				get_supplier_user=UserProfile.objects.filter(user_type__type_name='supplier').order_by('-id')
			
			return render(request, self.template_name,{'get_supplier_user':get_supplier_user,'from_date':from_date,'to_date':to_date})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		


@method_decorator(login_required, name="dispatch")
class EditCustomer(generic.TemplateView):
	template_name = 'admin/manage-member/edit-customer.html'


	def get(self, request,*args,id, **kwargs):
		if request.user.is_superuser:

			get_customer_instance=get_object_or_404(UserProfile,id=id)
			get_user_type=UserType.objects.all()
			return render(request, self.template_name,{'get_user_type':get_user_type,'get_customer_instance':get_customer_instance})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))

	def post(self, request,*args,id, **kwargs):
		if request.user.is_superuser:
			
			name=request.POST['name']
			phone=request.POST['phone']
			usertype=request.POST['usertype']
			get_usertype=get_object_or_404(UserType,type_name=usertype)
			UserProfile.objects.filter(id=id).update(full_name=name,phone=phone,user_type=get_usertype)
			messages.success(request,"Successfully Updated")
			id=str(id)
			return redirect(BASE_URL + 'admin/manage-member/edit-customer/' + id)
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		


@method_decorator(login_required, name="dispatch")
class EditSupplier(generic.TemplateView):
	template_name = 'admin/manage-member/edit-supplier.html'


	def get(self, request,*args,id, **kwargs):
		if request.user.is_superuser:
			get_supplier_instance=get_object_or_404(UserProfile,id=id)
			get_user_type=UserType.objects.all()
		
			return render(request, self.template_name,{'get_user_type':get_user_type,'get_supplier_instance':get_supplier_instance})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	
	def post(self, request,*args,id, **kwargs):
		if request.user.is_superuser:
		
			name=request.POST['name']
			phone=request.POST['phone']
			usertype=request.POST['usertype']
			get_usertype=get_object_or_404(UserType,type_name=usertype)
			UserProfile.objects.filter(id=id).update(full_name=name,phone=phone,user_type=get_usertype)
			messages.success(request,"Successfully Updated")
			id=str(id)
			return redirect(BASE_URL + 'admin/manage-member/edit-supplier/' + id)
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))	

@method_decorator(login_required, name="dispatch")
class ViewServices(generic.TemplateView):
	template_name = 'admin/manage-member/view-services.html'
	form = SupplierServicesForm


	def get(self, request,*args,id, **kwargs):
		if request.user.is_superuser:
			get_supplier_instance=get_object_or_404(UserProfile,id=id)
			get_tailor_spec=TailorSpecification.objects.all()
			get_supplier_services=SupplierServices.objects.filter(user_id=get_supplier_instance.user_id)

		
			return render(request, self.template_name,{'get_supplier_services':get_supplier_services,'get_supplier_instance':get_supplier_instance,'form': self.form,'get_tailor_spec':get_tailor_spec})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
	def post(self, request, id ,*args, **kwargs):

		phone = request.POST['phone']
		tailor_spec = request.POST['tailor_spec']
		get_tailor_spec_instance=get_object_or_404(TailorSpecification,id=tailor_spec)
		
		userprofile_instance = get_object_or_404(UserProfile,id=id)
		if UserProfile.objects.filter(phone=phone).filter(~Q(id=id)).exists():
		   
			messages.error(request, phone + ' Phone number already exists', )
		elif SupplierServices.objects.filter(tailor_speci_id=get_tailor_spec_instance).filter(Q(user_id=userprofile_instance.user_id)).exists():
		   
			messages.error(request, get_tailor_spec_instance.tailor_speci+' already exists', )
		else:
			
			userprofile_instance.phone = phone
			userprofile_instance.save()
			get_supplierservices_form = self.form(request.POST)
		  
			if get_supplierservices_form.is_valid():
				
				saveservices_data = get_supplierservices_form.save(commit=False)

				if 'yes' == request.POST['flexRadioDefault']:
					saveservices_data.ship_outside_country = "True"
				else:
					saveservices_data.ship_outside_country = "False"

				saveservices_data.user_id = userprofile_instance.user_id
				saveservices_data.created_by = request.user
				saveservices_data.tailor_speci_id=get_tailor_spec_instance
				saveservices_data.save()
				get_supplierservices_form.save_m2m()
				messages.success(request, 'Service Successfully added')
			else:
			  
				messages.error(request, ' Service can not be add', )
		id=str(id)	    
		return redirect(BASE_URL+'admin/manage-member/view-services/'+id)
		
		

@method_decorator(login_required, name="dispatch")
class ViewProducts(generic.TemplateView):
	
	template_name = 'admin/manage-member/view-products.html'


	def get(self, request,*args,id, **kwargs):
		if request.user.is_superuser:
			get_supplier_instance=get_object_or_404(UserProfile,id=id)
			get_supplier_products=SupplierProduct.objects.filter(user_id=get_supplier_instance.user_id)
			get_product_cate=Product_category.objects.all()

		
			return render(request, self.template_name,{'get_product_cate':get_product_cate,'get_supplier_products':get_supplier_products,'get_supplier_instance':get_supplier_instance})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		
		

@method_decorator(login_required, name="dispatch")
class ViewProductDetails(generic.TemplateView):
	template_name = 'admin/manage-member/view-product-details.html'


	def get(self, request,*args,id, **kwargs):
		if request.user.is_superuser:
			get_product_instance=get_object_or_404(SupplierProduct,id=id)
			jsonDec = json.decoder.JSONDecoder()
			get_color_list=None
			if (get_product_instance.color):
				get_color_list = jsonDec.decode(get_product_instance.color)
			
			return render(request, self.template_name,{'get_product_instance':get_product_instance,'get_color_list':get_color_list})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		
	

@method_decorator(login_required, name="dispatch")
class ViewAnswers(generic.TemplateView):
	template_name = 'admin/manage-member/view-answers.html'


	def get(self, request,*args,id, **kwargs):
		if request.user.is_superuser:
			get_supplier_instance=get_object_or_404(UserProfile,id=id)
			# get_supplier_products=SupplierProduct.objects.filter(user_id=get_supplier_instance.user_id)
			# get_all_questions = QuestionsTable.objects.filter(question_for__type_name='supplier')
			get_answer=UserAnswerTable.objects.filter(user=get_supplier_instance.user_id)
			return render(request, self.template_name,{'get_answer':get_answer})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		
		


# @method_decorator(login_required, name="dispatch")
@login_required
def ChangeStatus(request):
	if request.user.is_superuser:

		userid = request.POST["userid"]
		userstatus = request.POST["userstatus"]

		if userstatus == "True":
			status = False
		else:
			status = True
		if UserProfile.objects.filter(id=userid).exists():
			
			UserProfile.objects.filter(id=userid).update(status=status)
		return JsonResponse({'message': 'Status Changed successfully.'})
	else:
		messages.error(request,"Please enter valid username and password")
		return HttpResponseRedirect(reverse('admin_login'))

@login_required
def ChangePaidStatus(request):
	if request.user.is_superuser:

		userid = request.GET["userid"]
		paidstatus = request.GET["paidstatus"]

		if paidstatus == "Paid":
			status = False
		else:
			status = True

		user_ins=get_object_or_404(UserProfile ,id=userid)
		
		if BahesPayment.objects.filter(user_id=user_ins.user_id).exists():
			
			BahesPayment.objects.filter(user_id=user_ins.user_id).update(payment_status=status)
			return JsonResponse({'message': 'Payment1 Status Changed successfully.'})
		else:
			payment_obj=BahesPayment(user_id=user_ins.user_id,payment_status=True)
			payment_obj.save()
			return JsonResponse({'message': 'Payment2 Status Changed successfully.'})
	else:
		messages.error(request,"Please enter valid username and password")
		return HttpResponseRedirect(reverse('admin_login'))

@method_decorator(login_required, name="dispatch")
class MemberDelete(generic.TemplateView):

	def post(self, request, id, *args, **kwargs):
		if request.user.is_superuser:

			member_instance = get_object_or_404(UserProfile, id=id)
		   
			User.objects.filter(id=member_instance.user_id.id).delete()
			return HttpResponseRedirect(reverse('manage_member:ManageCustomer'))
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))



@method_decorator(login_required, name="dispatch")
class MemberMultipleDelete(generic.TemplateView):
	
	def post(self, request,*args, **kwargs):
		if request.user.is_superuser:
			member_array=request.POST.getlist('member_array[]')
			
			for data in member_array:
				member_instance = get_object_or_404(UserProfile, id=data)
				
				User.objects.filter(id=member_instance.user_id.id).delete()
			
			return JsonResponse({'message': 'Deleted successfully.'})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))





@register.filter(name='get_services_count')
def answer_status(data):
	get_services_count = 0
	
	if SupplierServices.objects.filter(user_id=data.user_id).exists():
		get_services_count=SupplierServices.objects.filter(user_id=data.user_id).count()
	return get_services_count



@register.filter(name='get_product_count')
def answer_status(data):
	get_product_count = 0
	
	if SupplierProduct.objects.filter(user_id=data.user_id).exists():
		get_product_count=SupplierProduct.objects.filter(user_id=data.user_id).count()
	return get_product_count