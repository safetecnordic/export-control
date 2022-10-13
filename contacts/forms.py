from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from contacts.models import Contact

class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=128)
    email = forms.EmailField(max_length=64)
    phone = PhoneNumberField(blank=True)