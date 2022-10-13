from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from utils.converters import str_to_int_or_none
from regulations.forms import SearchForm
from django.views.generic.list import ListView
from django.views.generic import DetailView

from regulations.models import Category, Paragraph, Regulation, SubCategory, Regime
from regulations.search import search_paragraphs, filter_paragraphs


class SearchView(ListView):
    model = Paragraph
    paginate_by = 20
    template_name = "regulations/search_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_term"] = self.request.GET.get("q", "")
        context["search_form"] = SearchForm(self.request.GET)
        context["page_title"] = _("Search")
        return context

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        paragraphs = search_paragraphs(q) if q else Paragraph.get_root_nodes()
        paragraphs = filter_paragraphs(
            paragraphs,
            self.request.GET.get("category", None),
            self.request.GET.get("subcategory", None),
            self.request.GET.get("regime", None),
        )

        return paragraphs


class RegulationDetailView(DetailView):
    model = Regulation
    template_name_suffix = "_detail"
    slug_field = "code"
    slug_url_kwarg = "code"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = settings.SITE_NAME
        context["page_description"] = _("This is a test to see if the translations work")
        context["root_paragraphs"] = self.object.paragraphs.filter(depth=1)
        return super(RegulationDetailView, self).get_context_data(**kwargs)
