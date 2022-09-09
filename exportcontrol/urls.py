from django.conf import settings
from django.contrib import admin
from django.urls import path
from base.views import PresentationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", PresentationView.as_view(), name="presentation"),
]
