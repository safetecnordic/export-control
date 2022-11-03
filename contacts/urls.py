from django.urls import path
from django.views.generic import TemplateView
from contacts.views import AddContactView

urlpatterns = [
    path("", AddContactView.as_view(), name="consult"),
    path("success", TemplateView.as_view(template_name="contacts/thank_you.html"), name="success"),
]
