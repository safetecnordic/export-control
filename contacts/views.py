from django.shortcuts import render

def contact(request):
    context = dict()
    return render(request, 'contact_form.html', context)
