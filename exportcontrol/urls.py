import django
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from regulations.views import regulation_page, search_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include(django.conf.urls.i18n)),
]

urlpatterns += i18n_patterns(
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("", search_page, name="search_page"),
    path("regulation/<str:regulation_code>", regulation_page, name="regulation_page"),
    path("about-us/", TemplateView.as_view(template_name="base/about_us.html"), name="about_us"),
    path("contact-us/", TemplateView.as_view(template_name="base/contact_us.html"), name="contact_us"),
    path("export/", TemplateView.as_view(template_name="base/export_control_law.html"), name="export_control_law"),
)

if settings.DEBUG:
    import debug_toolbar  # type: ignore

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
