from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from admin_settings.models import System_settings
from .models import *
from django.contrib import messages
from django.template.loader import render_to_string, get_template
import smtplib
import email.message
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import requests
from bahes import settings
from manage_admin_settings.models import *
# Create your views here.
class Contact(generic.TemplateView):
	template_name = "contactus/contact-us.html"

	def get(self, request, *args, **kwargs):
		get_system_settings = System_settings.objects.all()

		return render(request, self.template_name,{'get_system_settings':get_system_settings})

	def post(self, request, *args, **kwargs):
		if 'name' and 'email'  and 'message' in request.POST:
			name=request.POST['name']
			email=request.POST['email']
			message=request.POST['message']
		   
			data_content = {"username": name,
									"email":email,
			                    "message": message }
			email_content = 'email_template/contact-us-email.html'

			email_template = get_template(email_content).render(data_content)
			# reciver_email = 'shiveshbhardwaj149@gmail.com'

			Subject = "You've got a new user query"
			
			if Email_Setting.objects.filter(status=True).exists():
				email_data = Email_Setting.objects.filter(status=True)
				for data in email_data:
					EMAIL_HOST = data.smtp_host
					EMAIL_PORT = data.smtp_port
					EMAIL_HOST_USER = data.smtp_username
					EMAIL_HOST_PASSWORD = data.smtp_password
			email_msg = EmailMessage(Subject, email_template, EMAIL_HOST_USER, [EMAIL_HOST_USER],
									 reply_to=[EMAIL_HOST_USER])
			email_msg.content_subtype = 'html'
			email_msg.send(fail_silently=False)
			contactusdata=ContactUs(name=name,email=email,message=message)
			contactusdata.save()
			messages.success(request, 'Message successfully sent')
		else:
			messages.error(request, 'Something going wrong')
		return HttpResponseRedirect(reverse('contactus:Contact'))

		