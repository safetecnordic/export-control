from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic.list import ListView

from regulations.forms import SearchForm
from regulations.models import Paragraph, Regulation
from regulations.search import search_paragraphs, filter_paragraphs


class SearchView(ListView):
    model = Paragraph
    paginate_by = 20
    template_name = "regulations/search_page.html"
    form = SearchForm()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        context["search_term"] = self.request.GET.get("q", "")
        context["page_title"] = _("Search")
        context["advanced"] = self.request.GET.get("advanced", False) == "true"
        return context

    def get_queryset(self):
        self.form = SearchForm(self.request.GET)
        paragraphs = list()
        query = self.request.GET.get("as_q", "")
        if self.form.is_valid() and query:
            paragraphs = search_paragraphs(query)
            paragraphs = filter_paragraphs(
                paragraphs,
                self.request.GET.get("category", None),
                self.request.GET.get("subcategory", None),
                self.request.GET.get("regime", None),
            )
        else:
            for error in self.form.errors:
                messages.error(self.request, f"{error.title()}: {self.form.errors[error]}")
        return paragraphs


class RegulationDetailView(DetailView):
    model = Regulation
    template_name_suffix = "_detail"
    slug_field = "code"
    slug_url_kwarg = "code"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["root_paragraphs"] = self.object.paragraphs.filter(depth=1)
        return context
