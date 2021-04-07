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
		



@register.filter(name='answer_status')
def answer_status(data):
	get_answer_status = 'No'
	
	if UserAnswerTable.objects.filter(user=data.user_id).exists():
		get_answer_status='Yes'
	return get_answer_status



@register.filter(name='paid_status')
def paid_status(data):
	
	get_paid_status = 'Unpaid'
	if BahesPayment.objects.filter(user_id=data.user_id).exists():
		get_paid_status='Paid'
	
	return get_paid_status


@method_decorator(login_required, name="dispatch")
class ManageSupplier(generic.TemplateView):
	template_name = 'admin/manage-member/manage-supplier.html'


	def get(self, request,*args, **kwargs):
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
		


@method_decorator(login_required, name="dispatch")
class EditCustomer(generic.TemplateView):
	template_name = 'admin/manage-member/edit-customer.html'


	def get(self, request,*args,id, **kwargs):

		get_customer_instance=get_object_or_404(UserProfile,id=id)
		get_user_type=UserType.objects.all()
		return render(request, self.template_name,{'get_user_type':get_user_type,'get_customer_instance':get_customer_instance})

	def post(self, request,*args,id, **kwargs):
		
		name=request.POST['name']
		phone=request.POST['phone']
		usertype=request.POST['usertype']
		get_usertype=get_object_or_404(UserType,type_name=usertype)
		UserProfile.objects.filter(id=id).update(full_name=name,phone=phone,user_type=get_usertype)
		messages.success(request,"Successfully Updated")
		id=str(id)
		return redirect(BASE_URL + 'admin/manage-member/edit-customer/' + id)
		


@method_decorator(login_required, name="dispatch")
class EditSupplier(generic.TemplateView):
	template_name = 'admin/manage-member/edit-supplier.html'


	def get(self, request,*args,id, **kwargs):
		get_supplier_instance=get_object_or_404(UserProfile,id=id)
		get_user_type=UserType.objects.all()
	
		return render(request, self.template_name,{'get_user_type':get_user_type,'get_supplier_instance':get_supplier_instance})
	
	def post(self, request,*args,id, **kwargs):
		
		name=request.POST['name']
		phone=request.POST['phone']
		usertype=request.POST['usertype']
		get_usertype=get_object_or_404(UserType,type_name=usertype)
		UserProfile.objects.filter(id=id).update(full_name=name,phone=phone,user_type=get_usertype)
		messages.success(request,"Successfully Updated")
		id=str(id)
		return redirect(BASE_URL + 'admin/manage-member/edit-supplier/' + id)	

@method_decorator(login_required, name="dispatch")
class ViewServices(generic.TemplateView):
	template_name = 'admin/manage-member/view-services.html'


	def get(self, request,*args,id, **kwargs):
		get_supplier_instance=get_object_or_404(UserProfile,id=id)
		get_supplier_services=SupplierServices.objects.filter(user_id=get_supplier_instance.user_id)

	
		return render(request, self.template_name,{'get_supplier_services':get_supplier_services})
		
		

@method_decorator(login_required, name="dispatch")
class ViewProducts(generic.TemplateView):
	template_name = 'admin/manage-member/view-products.html'


	def get(self, request,*args,id, **kwargs):
		get_supplier_instance=get_object_or_404(UserProfile,id=id)
		get_supplier_products=SupplierProduct.objects.filter(user_id=get_supplier_instance.user_id)

	
		return render(request, self.template_name,{'get_supplier_products':get_supplier_products})
		
		

@method_decorator(login_required, name="dispatch")
class ViewProductDetails(generic.TemplateView):
	template_name = 'admin/manage-member/view-product-details.html'


	def get(self, request,*args,id, **kwargs):
		get_product_instance=get_object_or_404(SupplierProduct,id=id)
		jsonDec = json.decoder.JSONDecoder()
		get_color_list=None
		if (get_product_instance.color):
			get_color_list = jsonDec.decode(get_product_instance.color)
		
		return render(request, self.template_name,{'get_product_instance':get_product_instance,'get_color_list':get_color_list})
		
	

@method_decorator(login_required, name="dispatch")
class ViewAnswers(generic.TemplateView):
	template_name = 'admin/manage-member/view-answers.html'


	def get(self, request,*args,id, **kwargs):
		get_supplier_instance=get_object_or_404(UserProfile,id=id)
		# get_supplier_products=SupplierProduct.objects.filter(user_id=get_supplier_instance.user_id)
		# get_all_questions = QuestionsTable.objects.filter(question_for__type_name='supplier')
		get_answer=UserAnswerTable.objects.filter(user=get_supplier_instance.user_id)
		return render(request, self.template_name,{'get_answer':get_answer})
		
		


# @method_decorator(login_required, name="dispatch")

def ChangeStatus(request):

		userid = request.POST["userid"]
		userstatus = request.POST["userstatus"]

		if userstatus == "True":
			status = False
		else:
			status = True
		if UserProfile.objects.filter(id=userid).exists():
			
			UserProfile.objects.filter(id=userid).update(status=status)
		return JsonResponse({'message': 'Status Changed successfully.'})



@method_decorator(login_required, name="dispatch")
class MemberDelete(generic.TemplateView):

	def post(self, request, id, *args, **kwargs):

		member_instance = get_object_or_404(UserProfile, id=id)
	   
		User.objects.filter(id=member_instance.user_id.id).delete()
		return HttpResponseRedirect(reverse('manage_member:ManageCustomer'))



@method_decorator(login_required, name="dispatch")
class MemberMultipleDelete(generic.TemplateView):
	
	def post(self, request,*args, **kwargs):
		member_array=request.POST.getlist('member_array[]')
		
		for data in member_array:
			member_instance = get_object_or_404(UserProfile, id=data)
			
			User.objects.filter(id=member_instance.user_id.id).delete()
		
		return JsonResponse({'message': 'Deleted successfully.'})
