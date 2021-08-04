# Import some useful packages.
from django.urls import path
from django.contrib.auth.models import User, auth
from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.FindSupplier.as_view(), name="FindSupplier"),
path('customer-payment/', views.Payment.as_view(), name="Payment"),
path('customer-payment-process', views.SendPayment.as_view(), name="SendPayment"),
path('customer-payment-done/', views.PaymentDone.as_view(), name="PaymentDone"),
path('supplier-view/<int:id>', views.SupplierView.as_view(), name="SupplierView"),
# path('payement', views.send_payment, name="send_payment"),
]