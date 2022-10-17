from django.urls import path
from django.views.generic import TemplateView
from contacts.views import AddContactView

urlpatterns = [
    path("add/", AddContactView.as_view(), name="add_contact"),
    path("thank-you/", TemplateView.as_view(template_name="contacts/thank_you.html"), name="thank_you"),
]
