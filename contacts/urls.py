from django.urls import path
from django.conf import settings
from django.conf.urls import include
from contacts.views import send_contact, AddContactView

urlpatterns = [
    path('add-contact',  AddContactView.as_view(),  name = 'add_contact'),
    #path('', ContactFormView.as_view(), name = 'add_contact')
]


if settings.DEBUG:
    import debug_toolbar  # type: ignore

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]