from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from contacts.models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "message"]