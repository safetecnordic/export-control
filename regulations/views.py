from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from regulations.models import Category, Paragraph, SubCategory, Regime
from .search import search_paragraphs, filter_paragraphs
from utils.converters import str_to_int_or_none
from regulations.forms import SearchForm
from django.views.generic.list import ListView


class SearchView(ListView):
    model = Paragraph
    paginate_by = 100
    template_name = "regulations/search_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        context["page_title"] = _("Search")
        return context

    def get_queryset(self):
        q = self.request.GET.get("q", "")

        category = self.request.GET.get("category", "")
        subcategory = self.request.GET.get("subcategory", "")
        regime = self.request.GET.get("regime", "")

        paragraphs = search_paragraphs(q) if q else Paragraph.get_root_nodes()
        paragraphs = filter_paragraphs(paragraphs, category, subcategory, regime)

        return paragraphs
