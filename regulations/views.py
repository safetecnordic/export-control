from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic.list import ListView

from regulations.forms import SearchForm
from regulations.models import Paragraph, Regulation
from regulations.search import get_searched_paragraphs, get_filtered_paragraphs


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
        if self.form.is_valid() and "as_q" in self.request.GET.keys() and self.request.GET.get("as_q", ""):
            paragraphs = Paragraph.objects.all()
            paragraphs = get_filtered_paragraphs(self.form.cleaned_data, paragraphs)
            paragraphs = get_searched_paragraphs(self.form.cleaned_data, paragraphs)
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
        context["root_paragraphs"] = self.object.paragraphs.filter(depth=1)
        return context
