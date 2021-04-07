from django.shortcuts import render,get_object_or_404
from django.views import generic
from admin_settings.models import System_settings
from .models import *
# Create your views here.
class About_Us(generic.TemplateView):
	template_name = "custom_app/about-us.html"

	def get(self, request, *args, **kwargs):
		get_system_settings = System_settings.objects.all()
		get_aboutus_data=get_privacy_policy=get_object_or_404(CustomPage,slug='about-us')
		
		return render(request, self.template_name,{'get_system_settings':get_system_settings,'get_aboutus_data':get_aboutus_data})
		

	   
	  

class PrivacyPolicy(generic.TemplateView):
	template_name = "custom_app/privacy-policy.html"

	def get(self, request, *args, **kwargs):
		get_system_settings = System_settings.objects.all()
		get_privacy_policy=get_object_or_404(CustomPage,slug='privacy-policy')
		return render(request, self.template_name,{'get_system_settings':get_system_settings,'get_privacy_policy':get_privacy_policy})
		
	  

class TermsOfServices(generic.TemplateView):
	template_name = "custom_app/terms-of-services.html"

	def get(self, request, *args, **kwargs):
		get_system_settings = System_settings.objects.all()
		get_termsofservices=get_object_or_404(CustomPage,slug='terms-of-services')
		return render(request, self.template_name,{'get_system_settings':get_system_settings,'get_termsofservices':get_termsofservices})
		
	  		

class Faq(generic.TemplateView):
	template_name = "custom_app/faq.html"

	def get(self, request, *args, **kwargs):
		get_system_settings = System_settings.objects.all()
		return render(request, self.template_name,{'get_system_settings':get_system_settings})
		
	  
	   