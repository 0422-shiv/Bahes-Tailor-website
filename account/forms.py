from django.contrib.auth.forms import PasswordChangeForm
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserForm(UserCreationForm):
   
    username = forms.EmailField(error_messages={'required': 'Please let us know what to call you!'},max_length=50,required=True, widget=forms.EmailInput(attrs={"type":"email","class":"input-style", 'name':'username', 'placeholder':'Email' }))

    password1 = forms.CharField(max_length=12, required=True, widget=forms.PasswordInput(
        attrs={"class": "input-style", 'name': 'pass', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=12, required=True, widget=forms.PasswordInput(
        attrs={"class": "input-style", 'name': 'confirmpass', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username','password1', 'password2']


class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(
            attrs={"class": "input-style", 'name': 'fullname', 'placeholder': 'Full Name'}))
    # tel_code = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={"class": "input-style set_number_only tel_code",'id':'tel', 'name': 'tel_code', 'placeholder': 'xxx',
    #                'maxlength': "6"}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-style set_number_only pho_register", 'name': 'phone', 'placeholder': 'Mob','maxlength':"11","id":"phone",'autocomplete':"off",'data-intl-tel-input-id':"0"}))
    country = forms.ModelChoiceField(required=True, empty_label="Select Country", queryset=Countries.objects.all(),
                                     widget=forms.Select(attrs={"class": "input-style country", 'name': 'country'}))

    class Meta:
        model = UserProfile
        fields = ['full_name','phone', 'country']


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", 'type':"Password", 'placeholder': "Old Password"}))
    new_password1 = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", 'type':"Password", 'placeholder': "New Password"}))
    new_password2 = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", 'type':"Password", 'placeholder': "Confirm Password"}))