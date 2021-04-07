from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import *
from findsupplier.models import *
from services.models import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from django.template.defaulttags import register
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name="dispatch")
class AdminDashboard(generic.TemplateView):
	template_name = 'admin/admin-dashboard/dashboard.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			get_customer=UserProfile.objects.filter(user_type__type_name='customer').order_by('-id')
			get_supplier=UserProfile.objects.filter(user_type__type_name='supplier').order_by('-id')
			get_services=TailorSpecification.objects.all()
			# newly_registered_customer=UserProfile.objects.filter(user_type__type_name='customer').order_by('-id')
			return render(request, self.template_name,{'get_customer':get_customer,'get_supplier':get_supplier,'get_services':get_services})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		

