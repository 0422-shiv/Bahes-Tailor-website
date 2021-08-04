from django.urls import path
from django.contrib.auth.models import User, auth
from . import views

urlpatterns = [
    path('', views.Product.as_view(), name='product'),
    path('post-products', views.PostProduct.as_view(), name='PostProduct'),
    path('category/<int:id>', views.GetProductCategory.as_view(), name='GetProductCategory'),
    path('subcategory/<int:id>/<str:slug>', views.GetSubProductCategory.as_view(), name='GetSubProductCategory'),
    path('delete/<int:id>', views.ProductDelete.as_view(), name='ProductDelete'),
    path('productstatus', views.ProductStatus.as_view(), name='ProductStatus'),
    path('edit-product/<int:id>', views.ProductEdit.as_view(), name='ProductEdit'),

]
