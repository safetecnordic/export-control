from django.views.generic import TemplateView
from regulations.forms import SearchForm
from django.urls import reverse

from base.models import ExtendedFlatPage


class FrontPageView(TemplateView):
    template_name = "base/front_page.html"

    def get_context_data(self, **kwargs):
        context = super(FrontPageView, self).get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        context["form_action"] = reverse("search")
        context["flatpage"], new = ExtendedFlatPage.objects.get_or_create(url="/home/")
        return context
