from django.views.generic import TemplateView


class PresentationView(TemplateView):
    template_name = "base/presentation.html"

    def get_context_data(self, **kwargs):
        context = super(PresentationView, self).get_context_data(**kwargs)
        context["page_title"] = "ExportControl"
        return context
