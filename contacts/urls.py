from django.urls import path

from contacts.views import send_contact

urlpatterns = [
    path('', send_contact, name='contact')
]