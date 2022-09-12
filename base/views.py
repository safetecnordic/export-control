from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class PresentationView(TemplateView):
    template_name = "base/presentation.html"

    def get_context_data(self, **kwargs):
        context = super(PresentationView, self).get_context_data(**kwargs)
        context["page_title"] = _("ExportControl")
        context["page_description"] = _("This is a test to see if the translations work")
        return context
