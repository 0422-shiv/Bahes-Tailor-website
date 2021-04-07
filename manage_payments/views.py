from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import *
from findsupplier.models import *
from survey.models import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from django.template.defaulttags import register

# @method_decorator(login_required, name="dispatch")
class ManageCost(generic.TemplateView):
	template_name = 'admin/manage-payments/manage-cost.html'


	def get(self, request,*args, **kwargs):

	
		return render(request, self.template_name)
		

class ManageOrder(generic.TemplateView):
	template_name = 'admin/manage-payments/manage-order.html'


	def get(self, request,*args, **kwargs):

	
		return render(request, self.template_name)