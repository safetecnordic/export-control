from re import template
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.views.generic import TemplateView
from contacts.views import AddContactView

urlpatterns = [
    path('add-contact/',  AddContactView.as_view(),  name='add_contact'),
    path('thank-you/', TemplateView.as_view(template_name="thank_you.html"), name = 'thank_you')
]

if settings.DEBUG:
    import debug_toolbar  # type: ignore

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]