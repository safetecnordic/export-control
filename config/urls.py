from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.contrib.flatpages.views import flatpage


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("i18n/", include("django.conf.urls.i18n")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + i18n_patterns(
        path("", flatpage, kwargs={"url": "/"}, name="home"),
        path("about/", flatpage, kwargs={"url": "/about/"}, name="about"),
        path("regimes/", flatpage, kwargs={"url": "/regimes/"}, name="regimes"),
        path("knowledge-transfer/", flatpage, kwargs={"url": "/knowledge-transfer/"}, name="knowledge-transfer"),
        path("regulations/", include("regulations.urls")),
        path("consult/", include("contacts.urls")),
    )
)

if settings.DEBUG:
    import debug_toolbar  # type: ignore

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
