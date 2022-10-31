from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView

from contacts.forms import ContactForm
from contacts.models import Contact
from django.contrib.flatpages.models import FlatPage

class AddContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/add_contact.html"
    success_url = reverse_lazy("thank_you")

    def get_context_data(self, *args, **kwargs):
        context = super(AddContactView, self).get_context_data(**kwargs)
        #context["page_title"] = _("Consult Safetech")
        context["flatpage"] = FlatPage.objects.get(url='/consult/')
        return context
