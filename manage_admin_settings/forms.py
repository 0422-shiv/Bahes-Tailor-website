from django import forms
from .models import Email_Setting


# Create form for email settings for admin panel.
class EmailSettingForm(forms.ModelForm):
    smtp_host = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'placeholder':"SMTP Host", 'name': 'smtp_host'}))
    smtp_username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'placeholder':"SMTP Username", 'name': 'smtp_username'}))
    smtp_password = forms.CharField(widget=forms.TextInput(attrs={"type":"password","class": "form-control",'placeholder':"SMTP Password", 'name': 'smtp_password'}))
    smtp_port = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",'placeholder':"SMTP Port", 'name': 'smtp_port'}))

    class Meta:
        model = Email_Setting
        fields = ['smtp_host', 'smtp_username', 'smtp_password', 'smtp_port']

