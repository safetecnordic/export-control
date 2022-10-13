from .forms import ContactForm
from contacts.models import Contact
from django.views.generic.edit import CreateView

from django.shortcuts import redirect, render
from django.urls import reverse

def send_contact(request):
    contact_form = ContactForm()
    if request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            email = contact_form.cleaned_data["email"]
            name = contact_form.cleaned_data["name"]
            message = contact_form.cleaned_data["message"]
            contact = Contact(name=name, email=email, message = message)
            contact.save()
            return redirect(reverse('search_page'))
    context = {"form": contact_form}
    return render(request, "contact_form.html", context) 
#class ContactFormView(CreateView):
 #   template_name = 'contact_form.html'
  #  form_class = ContactForm
   # success_url =  "/" #reverse('search_page')

    #def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
     #   form.save_contact()
      #  return super().form_valid(form)