from django.contrib.postgres.search import SearchVector, SearchQuery, SearchHeadline
from treebeard.mp_tree import MP_NodeManager
from django.db.models import Q
from django.conf import settings


FIELD_TO_SEARCH = "text"


class SearchQueries:
    query: SearchQuery | None
    and_query: SearchQuery | None
    or_query: SearchQuery | None
    not_query: SearchQuery | None

    category_query: str | None
    subcategory_query: str | None
    regime_query: str | None
    type_query: str | None

    def __init__(self, search_params: dict[str, str]):
        query_param = search_params.get("as_q")
        self.query = SearchQuery(query_param, config=settings.DB_SEARCH_CONFIG) if query_param else None

        and_query_param = search_params.get("as_qand")
        self.and_query = (
            SearchQuery(and_query_param, search_type="phrase", config=settings.DB_SEARCH_CONFIG)
            if and_query_param
            else None
        )

        or_query_param = search_params.get("as_qor")
        self.or_query = (
            SearchQuery(
                f"{query_param} {or_query_param}" if query_param else or_query_param,
                search_type="websearch",
                config=settings.DB_SEARCH_CONFIG,
            )
            if or_query_param
            else None
        )

        not_query_param = search_params.get("as_qnot")
        self.not_query = (
            SearchQuery(not_query_param, search_type="websearch", config=settings.DB_SEARCH_CONFIG)
            if not_query_param
            else None
        )

        self.category_query = search_params.get("as_cat")
        self.subcategory_query = search_params.get("as_subcat")
        self.regime_query = search_params.get("as_reg")
        self.type_query = search_params.get("as_type")


def highlight_paragraphs(paragraphs: MP_NodeManager, queries: SearchQueries) -> MP_NodeManager:
    for search_query in [queries.query, queries.and_query, queries.or_query]:
        if search_query is None:
            continue

        search_headline = SearchHeadline(FIELD_TO_SEARCH, search_query, config=settings.DB_SEARCH_CONFIG)
        paragraphs = paragraphs.annotate(headline=search_headline)

    return paragraphs


def filter_paragraphs(paragraphs: MP_NodeManager, queries: SearchQueries) -> MP_NodeManager:
    if queries.category_query:
        paragraphs = paragraphs.filter(
            Q(category=queries.category_query) | Q(regulation__category=queries.category_query)
        )

    if queries.subcategory_query:
        paragraphs = paragraphs.filter(
            Q(sub_category=queries.subcategory_query) | Q(regulation__sub_category=queries.subcategory_query)
        )

    if queries.regime_query:
        paragraphs = paragraphs.filter(regulation__regime=queries.regime_query)

    if queries.type_query and queries.type_query != "base":
        paragraphs = paragraphs.filter(note_type=queries.type_query)

    search_vector = SearchVector(FIELD_TO_SEARCH, config=settings.DB_SEARCH_CONFIG)
    paragraphs = paragraphs.annotate(search=search_vector)

    if queries.query:
        paragraphs = paragraphs.filter(search=queries.query)
    if queries.and_query:
        paragraphs = paragraphs.filter(search=queries.and_query)
    if queries.or_query:
        paragraphs = paragraphs.filter(search=queries.or_query)
    if queries.not_query:
        paragraphs = paragraphs.exclude(search=queries.not_query)

    paragraphs = paragraphs.order_by("-depth")

    return paragraphs
