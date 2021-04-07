# Import some useful packages.
from django.urls import path
from django.contrib.auth.models import User, auth
from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.About_Us.as_view(), name="AboutUs"),
path('privacy-policy', views.PrivacyPolicy.as_view(), name="PrivacyPolicy"),
path('terms-of-use', views.TermsOfServices.as_view(), name="TermsOfServices"),
path('faq', views.Faq.as_view(), name="Faq"),

]