from concurrent.futures.process import _python_exit
from django.shortcuts import redirect, render

from django.contrib import messages
from contacts.models import Contact

def contact(request):
    context = dict()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()

        messages.success(request, "Thank you for your request, we get back to you soon!")
        return redirect(request.META.get('HTTP_REFERER'))


