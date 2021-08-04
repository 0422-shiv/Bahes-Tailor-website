from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from admin_settings.models import System_settings
from services.models import *
from products.models import *
from account.models import *
from findsupplier.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import simplejson as json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.
class FindProducts(generic.TemplateView):
	template_name = "findproducts/find-products.html"

	def get(self, request, *args, **kwargs):
		get_system_settings = System_settings.objects.all()
		get_tailor_services=TailorSpecification.objects.filter(status=True)
		get_products_subcat=Product_subcategory.objects.all()
		q_list=['Latest','By Price','Oldest']
		get_fabric_product=get_object_or_404(Product_category,slug='fabrics')
		q_sort_by=''
		get_filter_products_subcat=''
		get_filter_fabric_product=''
		if 'product' in request.GET or 'sort-by' in request.GET:

			if 'product' in request.GET and 'sort-by' in request.GET:
					q_sort_by = self.request.GET['sort-by']
					q = self.request.GET.getlist('product')
					# print('sbdvjhbsdvhjbwvj')
					if q_sort_by == 'Latest':
						get_prod = SupplierProduct.objects.filter(Q(Product_subcategory__subcategory_name__in=q) | Q(product_category__category_name__in=q)).filter(status=True).order_by('-id')

					elif q_sort_by == 'By Price':
						get_prod = SupplierProduct.objects.filter(Q(Product_subcategory__subcategory_name__in=q) | Q(product_category__category_name__in=q)).filter(status=True).order_by('price')

					elif q_sort_by == 'Oldest':
						get_prod = SupplierProduct.objects.filter(Q(Product_subcategory__subcategory_name__in=q) | Q(product_category__category_name__in=q)).filter(status=True).order_by('id')
					get_filter_products_subcat=Product_subcategory.objects.filter(subcategory_name__in=q)
					get_filter_fabric_product=Product_category.objects.filter(category_name__in=q)
			elif 'sort-by' in request.GET:
				# print('sort')
				q_sort_by = self.request.GET['sort-by']
				
				if q_sort_by == 'Latest':
					get_prod = SupplierProduct.objects.filter(status=True).order_by('-id')
				elif q_sort_by == 'By Price':
					get_prod = SupplierProduct.objects.filter(status=True).order_by('price')
				elif q_sort_by == 'Oldest':
					get_prod = SupplierProduct.objects.filter(status=True).order_by('id')
			elif 'product' in request.GET:
				# print('product')
				q = self.request.GET.getlist('product')
				get_prod = SupplierProduct.objects.filter(Q(Product_subcategory__subcategory_name__in=q) | Q(product_category__category_name__in=q)).filter(status=True)
				get_filter_products_subcat=Product_subcategory.objects.filter(subcategory_name__in=q)
				get_filter_fabric_product=Product_category.objects.filter(category_name__in=q)
			
		
		else:
			get_prod=SupplierProduct.objects.filter(status=True).order_by('-id')
			
		page = request.GET.get('page', 1)
		paginator = Paginator(get_prod, 12) 
			
			
		try:
			get_products = paginator.page(page)
		except PageNotAnInteger:
			get_products = paginator.page(1)
		except EmptyPage:
					
			get_products = paginator.page(paginator.num_pages)
		return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'get_prod':get_prod,'q_list':q_list,'q_sort_by':q_sort_by,'get_filter_fabric_product':get_filter_fabric_product,'get_products_subcat':get_products_subcat,'get_filter_products_subcat':get_filter_products_subcat,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_system_settings':get_system_settings})

			# return render(request, self.template_name,{'q_list':q_list,'get_products_subcat':get_products_subcat,'get_fabric_product':get_fabric_product,'get_products':get_products,'get_system_settings':get_system_settings})
		
	   

class ProductDetail(generic.TemplateView):
	template_name = "findproducts/product-detail.html"

	def get(self, request, id,*args, **kwargs):
		get_payment=None

		if request.user.is_authenticated:
			if BahesPayment.objects.filter(user_id=request.user).exists():
					get_payment=get_object_or_404(BahesPayment,user_id=request.user)
		get_system_settings = System_settings.objects.all()
		get_tailor_services=TailorSpecification.objects.filter(status=True)
		get_product_instance=get_object_or_404(SupplierProduct,id=id)
		jsonDec = json.decoder.JSONDecoder()
		get_color_list=None
		if (get_product_instance.color):
			get_color_list = jsonDec.decode(get_product_instance.color)
		return render(request, self.template_name,{'get_tailor_services':get_tailor_services,'get_payment':get_payment,'get_color_list':get_color_list,'get_product_instance':get_product_instance,'get_system_settings':get_system_settings})
		
