from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView

from .forms import ContactForm
from .models import Contact

def send_contact(request):
    contact_form = ContactForm()
    if request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect(reverse('search_page'))
    context = {"form": contact_form}
    return render(request, "contact_form.html", context) 

class AddContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact_form.html"
    #success_url = '/' # here should be reverse?
    def form_valid(self, form): # new
        return redirect(reverse('search_page'))