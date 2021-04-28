# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.ManageCustomer.as_view(), name="ManageCustomer"),
path('edit-customer/<int:id>', views.EditCustomer.as_view(), name="EditCustomer"),
path('manage-supplier', views.ManageSupplier.as_view(), name="ManageSupplier"),
path('edit-supplier/<int:id>', views.EditSupplier.as_view(), name="EditSupplier"),
path('view-services/<int:id>', views.ViewServices.as_view(), name="ViewServices"),
path('view-products/<int:id>', views.ViewProducts.as_view(), name="ViewProducts"),
path('view-product-details/<int:id>', views.ViewProductDetails.as_view(), name="ViewProductDetails"),
path('view-answers/<int:id>', views.ViewAnswers.as_view(), name="ViewAnswers"),
path('change-status', views.ChangeStatus, name="ChangeStatus"),
path('delete-member/<int:id>', views.MemberDelete.as_view(), name="MemberDelete"),
path('delete-multiple-member/', views.MemberMultipleDelete.as_view(), name="MemberMultipleDelete"),

]