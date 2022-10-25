
from django.shortcuts import render

def error_404(request, exception=None):
    return render(request, 'base/404.html')