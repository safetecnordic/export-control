from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from utils.converters import str_to_int_or_none
from .models import Category, Paragraph, Regulation, SubCategory, Regime
from .search import search_paragraphs, filter_paragraphs


def search_page(request: HttpRequest) -> HttpResponse:
    search_term = request.GET.get("q")
    page = str_to_int_or_none(request.GET.get("page"))
    category_id = str_to_int_or_none(request.GET.get("category"))
    subcategory_id = str_to_int_or_none(request.GET.get("subcategory"))
    regime_id = str_to_int_or_none(request.GET.get("regime"))

    paragraphs = search_paragraphs(search_term) if search_term else Paragraph.get_root_nodes()
    paragraphs = filter_paragraphs(paragraphs, category_id, subcategory_id, regime_id)
    paragraphs = Paginator(paragraphs, 10).get_page(page) if paragraphs else None

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    regimes = Regime.objects.all()

    category = Category.objects.get(id=category_id) if category_id else None
    subcategory = SubCategory.objects.get(id=subcategory_id) if subcategory_id else None
    regime = Regime.objects.get(id=regime_id) if regime_id else None

    context = {
        "page_title": settings.SITE_NAME,
        "page_description": _("This is a test to see if the translations work"),
        "search_term": search_term,
        "paragraphs": paragraphs,
        "categories": categories,
        "subcategories": subcategories,
        "regimes": regimes,
        "category": category,
        "subcategory": subcategory,
        "regime": regime,
    }

    return render(request, "search_page.html", context)


def regulation_page(request: HttpRequest, regulation_code: str) -> HttpResponse:
    regulation = Regulation.objects.get(code=regulation_code)
    paragraphs = regulation.paragraphs.all()

    context = {
        "page_title": settings.SITE_NAME,
        "page_description": _("This is a test to see if the translations work"),
        "regulation": regulation,
        "paragraphs": paragraphs,
    }

    return render(request, "regulation_page.html", context)
