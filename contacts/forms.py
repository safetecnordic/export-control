from django import forms
from django.utils.translation import gettext as _
from contacts.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone_number", "message"]
        required_fields = ["name", "email", "message"]
        labels = {
            "name": "",
            "email": "",
            "phone_number": "",
            "message": "",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Name*")}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email*")}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Phone Number")}),
            "message": forms.Textarea(attrs={"class": "form-control", "placeholder": _("Enter your message here...")}),
        }
