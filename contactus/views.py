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
			reciver_email = 'gaurav@digimonk.net'

			Subject = 'BAHES'
			email_msg = EmailMessage(Subject, email_template, settings.EMAIL_HOST_USER, [reciver_email],
			                             reply_to=[settings.EMAIL_HOST_USER])
			email_msg.content_subtype = 'html'
			email_msg.send(fail_silently=False)
			contactusdata=ContactUs(name=name,email=email,message=message)
			contactusdata.save()
			messages.success(request, 'Message successfully sent')
		else:
			messages.error(request, 'Something going wrong')
		return HttpResponseRedirect(reverse('contactus:Contact'))

		