from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from treebeard.mp_tree import MP_NodeManager
from regulations.models import Paragraph


def search_paragraphs(search_term: str) -> MP_NodeManager:
    field_to_search = "text"
    search_vector = SearchVector(field_to_search)
    search_query = SearchQuery(search_term)
    search_rank = SearchRank(search_vector, search_query)
    search_headline = SearchHeadline(field_to_search, search_query)
    paragraphs = (
        Paragraph.objects.annotate(rank=search_rank)
        .annotate(headline=search_headline)
        .filter(rank__gte=0.001)
        .order_by("-rank")
    )
    paragraphs = Paragraph.objects.annotate(search=search_vector).filter(search=search_query)
    return paragraphs


def filter_paragraphs(
    paragraphs: MP_NodeManager,
    category_id: int | None,
    subcategory_id: int | None,
    regime_id: int | None,
) -> MP_NodeManager:
    if category_id:
        paragraphs = paragraphs.filter(regulation__category__id=category_id)
    if subcategory_id:
        paragraphs = paragraphs.filter(regulation__sub_category__id=subcategory_id)
    if regime_id:
        paragraphs = paragraphs.filter(regulation__regime__id=regime_id)
    return paragraphs
