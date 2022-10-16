from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from .forms import ContactForm
from .models import Contact


class AddContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact_form.html"
    def form_valid(self, form): 
        form.save()
        return redirect(reverse('thank_you'))