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
    path("regulations/", include("regulations.urls")),
    path("contacts/", include("contacts.urls")),
    path("about-us/", TemplateView.as_view(template_name="base/about_us.html"), name="about_us"),
    path("export/", TemplateView.as_view(template_name="base/export_control_law.html"), name="export_control_law"),
    path("knowledge-transfer/", TemplateView.as_view(template_name="base/knowledge_transfer.html"), name="knowledge_transfer"),
    path("", PresentationView.as_view(), name="presentation"),
)

if settings.DEBUG:
    import debug_toolbar  # type: ignore

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
