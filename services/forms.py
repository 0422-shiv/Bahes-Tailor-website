from django import forms

from account.models import Countries
from .models import *



class SupplierServicesForm(forms.ModelForm):
    country_id = forms.ModelChoiceField(required=True, empty_label="Please select country",
                                        queryset=Countries.objects.all(),
                                        widget=forms.Select(attrs={"class": "form-control", 'name': 'country_id'}))

   
    tailor_experience=forms.CharField( required=True, widget=forms.TextInput(
            attrs={"type":"text",'maxlength':'12',"class": "form-control", 'name': 'tailor_experience', 'placeholder': 'enter tailor experience'}))

    address = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control",'id':"exampleFormControlTextarea1" ,'name': 'address' ,'rows':'4'}))

    class Meta:
        model = SupplierServices
        fields = ['country_id','tailor_experience', 'targeted_customer', 'tailor_staff_gender', 'address']

