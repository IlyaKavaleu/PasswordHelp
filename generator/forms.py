from django import forms
from .models import Password_Model


class PasswordForm(forms.ModelForm):
    """Form for REGISTRATION"""
    class Meta:
        model = Password_Model
        fields = ['text']
        labels = {'text': ''}


class ContactForm(forms.Form):
    """Form for SEND EMAIL"""
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
