import django
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from base.views import PresentationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include(django.conf.urls.i18n)),
]

urlpatterns += i18n_patterns(
    path("accounts/", include("django.contrib.auth.urls")),
    path("", PresentationView.as_view(), name="presentation"),
    path("about-us/", TemplateView.as_view(template_name="base/about_us.html"), name="about_us"),
    path("contact-us/", TemplateView.as_view(template_name="base/contact_us.html"), name="contact_us"),
]
)

if settings.DEBUG:
    import debug_toolbar  # type: ignore

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
