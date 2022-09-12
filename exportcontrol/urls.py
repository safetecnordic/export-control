from base.views import PresentationView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", PresentationView.as_view(), name="presentation"),
]

if settings.DEBUG:
    import debug_toolbar

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
