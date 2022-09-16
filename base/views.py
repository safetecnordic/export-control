from django.conf import settings
from django.utils.translation import gettext as _
from django.views.generic import TemplateView


class PresentationView(TemplateView):
    template_name = "base/presentation.html"

    def get_context_data(self, **kwargs):
        context = super(PresentationView, self).get_context_data(**kwargs)
        context["page_title"] = settings.SITE_NAME
        context["page_description"] = _("This is a test to see if the translations work")

        return context
