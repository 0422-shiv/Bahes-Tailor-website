
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from .models import *
from contactus.models import *
from django.contrib import messages
from .forms import EmailSettingForm
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import  get_template
import smtplib
import email.message
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from bahes import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from allauth.account.signals import password_changed
from django.dispatch import receiver


# @receiver(password_changed)
# def password_change_callback(sender, request, user, **kwargs):
#     messages.success(request, 'You have Successfully changed your Password!.')
# @method_decorator(login_required, name="dispatch")
# class ChangePassword(generic.TemplateView):
# 	template_name = 'admin/manage-admin-settings/change-password.html'


# 	def get(self, request,*args, **kwargs):

	
# 		return render(request, self.template_name)


# --------------------- Get SMTP Mail detail ----------------------------------
if Email_Setting.objects.filter(status=True).exists():
	email_data = Email_Setting.objects.filter(status=True)
	for data in email_data:
		EMAIL_HOST = data.smtp_host
		EMAIL_PORT = data.smtp_port
		EMAIL_HOST_USER = data.smtp_username
		EMAIL_HOST_PASSWORD = data.smtp_password
else:
	EMAIL_HOST = ""
	EMAIL_PORT = ""
	EMAIL_HOST_USER = ""
	EMAIL_HOST_PASSWORD = ""		

@method_decorator(login_required, name="dispatch")
class EmailSettings(generic.TemplateView):
	template_name = 'admin/manage-admin-settings/email-setting.html'


	def get(self, request,*args, **kwargs):
		email_setting_form = EmailSettingForm

		# Check email setting already exist or not.
		if Email_Setting.objects.filter(status=True).exists():
			email_value = get_object_or_404(Email_Setting, status=True)
			email_setting_form = EmailSettingForm(instance=email_value)
	
		return render(request, self.template_name,{'email_setting_form':email_setting_form,"username":request.user.username})

	def post(self, request):
		# Post function for add or update email setting.
		if EmailSettingForm(request.POST):
			email_setting_form = EmailSettingForm(request.POST)
			# Check email setting already exist or not.
			if Email_Setting.objects.filter(status=True).exists():
				email_value = get_object_or_404(Email_Setting, status=True)
				email_setting_form = EmailSettingForm(request.POST, instance=email_value)

			if email_setting_form.is_valid():
				data = email_setting_form.save(commit=False)
				data.updated_dt = datetime.now()
				data.save()
			messages.success(request,'Email succesfully updated')
		else:
			messages.error(request,'Email can not be updated')
		return HttpResponseRedirect(reverse('manage_admin_settings:EmailSettings'))

		
@method_decorator(login_required, name="dispatch")
class ManageEnquiries(generic.TemplateView):
	template_name = 'admin/manage-admin-settings/manage-enquiries.html'


	def get(self, request,*args, **kwargs):
		from_date=None
		to_date=None
		if 'from_date' in request.GET and 'to_date' in request.GET :
			from_date = request.GET['from_date']
			to_date = request.GET['to_date']
			
			from_date_format = datetime.strptime(from_date,"%m/%d/%Y")
			to_date_format = datetime.strptime(to_date,"%m/%d/%Y")
			
			get_enquiries=ContactUs.objects.filter(created_date__range=[from_date_format, to_date_format])
		else:
			get_enquiries=ContactUs.objects.all()
		return render(request, self.template_name,{'get_enquiries':get_enquiries,'from_date':from_date,'to_date':to_date})




@method_decorator(login_required, name="dispatch")
class EnquiryReply(generic.TemplateView):
	template_name = 'admin/manage-admin-settings/reply.html'


	def get(self, request,id,*args, **kwargs):
		
		get_instance=get_object_or_404(ContactUs,id=id)
		return render(request, self.template_name,{'get_instance':get_instance})

	def post(self, request,id,*args, **kwargs):
		subject=request.POST['subject']
		print(subject)
		comment=request.POST['description']
		get_instance=get_object_or_404(ContactUs,id=id)

		if User.objects.filter(email=get_instance.email).exists():
		   
			
			data_content = {"username": get_instance.name,
							"comment": comment}
			email_content = 'admin/email-pages/reply-email.html'

			email_template = get_template(email_content).render(data_content)
			reciver_email = get_instance.email

			Subject = subject
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
			get_instance.reply_status=True
			get_instance.save()
			messages.success(request, "successfully replied to "+get_instance.name+"")
		else:
			messages.error(request, "something going wrong please try again")
		return HttpResponseRedirect(reverse('manage_admin_settings:ManageEnquiries'))
		   


		
@method_decorator(login_required, name="dispatch")
class DeleteMultiEnquiries(generic.TemplateView):

	def post(self, request,*args, **kwargs):
		enquiries_array=request.POST.getlist('enquiries_array[]')
		
		for data in enquiries_array:
			enquiry_instance = get_object_or_404(ContactUs, id=data)
			
			ContactUs.objects.filter(id=enquiry_instance.id).delete()
		
		return JsonResponse({'message': 'Deleted successfully.'})