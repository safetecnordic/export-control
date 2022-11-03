import django
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from base.views import FrontPageView
from django.contrib.flatpages import views
from config.views import handler404


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("home/", handler404),
    path("consult/", handler404),
    path("regulations/", include("regulations.urls")),
    path("contacts/", include("contacts.urls")),
    path("", include("django.contrib.flatpages.urls")),
    path("", FrontPageView.as_view(), name="front_page"),
)


if settings.DEBUG:
    import debug_toolbar  # type: ignore

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
