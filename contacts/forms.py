from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from contacts.models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "message"]

        labels = {
            'name': '',
            'email': '',
            'phone': '',
            'message': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Phone'}),
            'message': forms.Textarea(attrs={'class': 'form-control','placeholder':'Enter your message here'})
        }