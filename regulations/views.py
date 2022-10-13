from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from utils.converters import str_to_int_or_none
from regulations.forms import SearchForm
from django.views.generic.list import ListView
from .models import Category, Paragraph, Regulation, SubCategory, Regime
from .search import search_paragraphs, filter_paragraphs


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


def regulation_page(request: HttpRequest, regulation_code: str) -> HttpResponse:
    regulation = Regulation.objects.get(code=regulation_code)
    root_paragraphs = regulation.paragraphs.filter(depth=1)

    context = {
        "page_title": settings.SITE_NAME,
        "page_description": _("This is a test to see if the translations work"),
        "regulation": regulation,
        "root_paragraphs": root_paragraphs,
    }

    return render(request, "regulation_page.html", context)
