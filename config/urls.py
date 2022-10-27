from tkinter import E
import django
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from base.views import FrontPageView
from django.contrib.flatpages import views
from config.views import error_404


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include('django.conf.urls.i18n')),
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("home/", error_404),   
    path("consult/", error_404),    
    path("regulations/", include("regulations.urls")),
    path("contacts/", include("contacts.urls")),
    #path("export/", TemplateView.as_view(template_name="base/export_control_law.html"), name="export_control_law"),
    path('knowledge-transfer/', views.flatpage, {'url': '/knowledge-transfer/'}, name="knowledge_transfer"),
    path('export-control-law/', views.flatpage, {'url': '/export/'}, name="export_control_law"),
    #path("knowledge-transfer/", TemplateView.as_view(template_name="base/knowledge_transfer.html"), name="knowledge_transfer"),
    path("", FrontPageView.as_view(), name="front_page"),
)

if settings.DEBUG:
    import debug_toolbar  # type: ignore

    # Allow error pages to be tested
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
