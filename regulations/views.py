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
        return context

    def get_queryset(self):
        self.form = SearchForm(self.request.GET)
        paragraphs = list()
        if self.form.is_valid():
            paragraphs = Paragraph.objects.all()
            paragraphs = get_filtered_paragraphs(self.form.cleaned_data, paragraphs)
            paragraphs = get_searched_paragraphs(self.form.cleaned_data, paragraphs)
            paragraphs = paragraphs.order_by("-depth")
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
