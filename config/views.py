from django.shortcuts import render


def handler404(request, exception=None):
    return render(request, "base/404.html", status=404)
