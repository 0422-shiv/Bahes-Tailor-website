from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import generic
from admin_settings.models import System_settings
from services.models import *
from account.models import *
from django.template.defaulttags import register
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.db.models import Count,Max
from django.template.loader import render_to_string
from django.db.models import Q
from django.db.models import Count
# Create your views here.
class FindServices(generic.TemplateView):
	template_name = "findservices/find-services.html"

	def get(self, request, *args, **kwargs):
		get_system_settings = System_settings.objects.all()
		get_tailor_services=TailorSpecification.objects.filter(status=True)
		get_services=SupplierServices.objects.filter(status=True)
		get_tailor_specilization=TailorSpecification.objects.filter(status=True).order_by('tailor_speci')
		q_sort_by=None
		get_tailor_spec=None
		get_tailor_sp=None
		get_tailor_specilization_list=[]
		if 'service' in request.GET and 'sort-by' in request.GET :
			q = self.request.GET.getlist('service')
			
			q_sort_by = self.request.GET['sort-by']
			
			if q_sort_by == 'Name':
				get_tailor_spec = TailorSpecification.objects.filter(tailor_speci__in=q).order_by('tailor_speci')
				page = request.GET.get('page', 1)
				paginator = Paginator(get_tailor_spec, 10)

		
		elif 'service'  in request.GET :
			q = self.request.GET.getlist('service')
			
			get_tailor_spec = TailorSpecification.objects.filter(tailor_speci__in=q).order_by('id')
			page = request.GET.get('page', 1)
			paginator = Paginator(get_tailor_spec, 10)

		
		elif 'sort-by' in request.GET :
			
			q_sort_by = self.request.GET['sort-by']
			
			if q_sort_by == 'Name':
				get_tailor_sp = TailorSpecification.objects.filter(status=True).order_by('tailor_speci')
				


		else:
			get_q=Q(supplier_tailor_speci__status=True)
			# get_tailor_specilization = TailorSpecification.objects.filter(status=True).order_by('tailor_speci')
			get_tailor_specilization=TailorSpecification.objects.annotate(service_count=Count('supplier_tailor_speci',get_q))
			print(get_tailor_specilization)
			for data in get_tailor_specilization:
				print(data)
				get_tailor_specilization_list.append(data.service_count)
			get_tailor_specilization_list = list(dict.fromkeys(get_tailor_specilization_list))
			get_tailor_specilization_list.sort(reverse=True)
			print(get_tailor_specilization_list)
			page = request.GET.get('page', 1)
			paginator = Paginator(get_tailor_specilization, 10) 
				
			
		try:
			get_tailor = paginator.page(page)
		except PageNotAnInteger:
			get_tailor = paginator.page(1)
		except EmptyPage:
					
			get_tailor = paginator.page(paginator.num_pages)
				
			
		return render(request, self.template_name,{'get_tailor_specilization_list':get_tailor_specilization_list,'get_tailor_services':get_tailor_services,'get_tailor_sp':get_tailor_sp,'q_sort_by':q_sort_by,'get_tailor_spec':get_tailor_spec,'get_tailor':get_tailor,'get_services':get_services,'get_tailor_specilization':get_tailor_specilization,'get_system_settings':get_system_settings})




@register.filter(name='get_supplier')
def get_supplier(data):
	get_supplier_data=None

	if SupplierServices.objects.filter(tailor_speci_id=data).exists():
	
		get_supplier_data=SupplierServices.objects.filter(tailor_speci_id=data).filter(status=True)
		get_supplier_count=SupplierServices.objects.filter(tailor_speci_id=data).filter(status=True).count()
		
	return render_to_string("findservices/get_supplier_data.html",{'get_supplier_data':get_supplier_data,'get_supplier_count':get_supplier_count})

		  

	

 