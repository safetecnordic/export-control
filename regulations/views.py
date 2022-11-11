from django.contrib import messages
from django.db.models import F
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic.list import ListView

from regulations.forms import SearchForm
from regulations.models import Paragraph, Regulation
from regulations.search import SearchQueries, highlight_paragraphs, filter_paragraphs
from base.models import ExtendedFlatPage


class SearchView(ListView):
    model = Paragraph
    paginate_by = 20
    template_name = "regulations/search_page.html"
    form = SearchForm()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get("as_q", "")
        context["search_form"] = SearchForm(self.request.GET)
        context["search_term"] = search_term
        context["page_title"] = _("Search")
        context["search_applied"] = (
            True
            if self.request.GET.get("as_q", False)
            or self.request.GET.get("as_qand", False)
            or self.request.GET.get("as_qnot", False)
            or self.request.GET.get("as_qor", False)
            else False
        )
        context["no_results"] = bool(search_term and not self.get_queryset())
        context["flatpage"], created = ExtendedFlatPage.objects.get_or_create(url="/search/")
        return context

    def get_queryset(self):
        self.form = SearchForm(self.request.GET)
        paragraphs = list()
        if self.form.is_valid():
            paragraphs = Paragraph.objects.filter(is_public=True)
            search_queries = SearchQueries(self.form.cleaned_data)
            paragraphs = filter_paragraphs(paragraphs, search_queries)
            paragraphs = highlight_paragraphs(paragraphs, search_queries)
        else:
            for error in self.form.errors:
                messages.error(self.request, f"{self.form.fields[error].label} {self.form.errors[error]}")
        return paragraphs


class RegulationDetailView(DetailView):
    model = Regulation
    template_name_suffix = "_detail"
    slug_field = "code"
    slug_url_kwarg = "code"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paragraphs"] = self.get_paragraphs()
        context["page_title"] = self.object.code
        context["flatpage"], created = ExtendedFlatPage.objects.get_or_create(url="/search/")
        return context

    def get_paragraphs(self):
        paragraphs = self.object.paragraphs

        form = SearchForm(self.request.GET)
        if form.is_valid():
            search_queries = SearchQueries(form.cleaned_data)
            paragraphs = highlight_paragraphs(paragraphs, search_queries)
        else:
            for error in form.errors:
                messages.error(self.request, f"{form.fields[error].label} {form.errors[error]}")

        paragraphs = paragraphs.annotate(margin=((F("depth") - 1) * 20))

        return paragraphs
