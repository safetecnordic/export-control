from django.contrib.postgres.search import SearchVector, SearchQuery, SearchHeadline
from treebeard.mp_tree import MP_NodeManager
from django.db.models import Q


def get_search_queries(as_q, as_qand, as_qor, as_qnot):
    query = None
    not_query = None
    and_query = None
    or_query = None
    if as_q:
        query = SearchQuery(as_q)
    if as_qand:
        and_query = SearchQuery(as_qand, search_type="phrase")
    if as_qor:
        if as_q:
            as_qor = f"{as_q} {as_qor}"
        or_query = SearchQuery(as_qor, search_type="websearch")
    if as_qnot:
        not_query = SearchQuery(as_qnot, search_type="websearch")
    return query, and_query, or_query, not_query


def get_searched_paragraphs(search_terms: dict, paragraphs: MP_NodeManager) -> MP_NodeManager:
    field_to_search = "text"
    search_vector = SearchVector(field_to_search)
    query, and_query, or_query, not_query = get_search_queries(
        search_terms["as_q"] if "as_q" in search_terms.keys() else None,
        search_terms["as_qand"] if "as_qand" in search_terms.keys() else None,
        search_terms["as_qor"] if "as_qor" in search_terms.keys() else None,
        search_terms["as_qnot"] if "as_qnot" in search_terms.keys() else None,
    )
    search_headline = SearchHeadline(field_to_search, query)
    paragraphs = paragraphs.annotate(search=search_vector).annotate(headline=search_headline)
    if query:
        paragraphs = paragraphs.filter(search=query)
    if and_query:
        search_headline = SearchHeadline(field_to_search, and_query)
        paragraphs = paragraphs.annotate(headline=search_headline).filter(search=and_query)
    if or_query:
        search_headline = SearchHeadline(field_to_search, or_query)
        paragraphs = paragraphs.annotate(headline=search_headline).filter(search=or_query)
    if not_query:
        paragraphs = paragraphs.exclude(search=not_query)

    return paragraphs


def get_filtered_paragraphs(search_terms: dict, paragraphs: MP_NodeManager) -> MP_NodeManager:
    if "as_cat" in search_terms.keys() and search_terms["as_cat"]:
        paragraphs = paragraphs.filter(
            Q(category=search_terms["as_cat"]) | Q(regulation__category=search_terms["as_cat"])
        )
    if "as_subcat" in search_terms.keys() and search_terms["as_subcat"]:
        paragraphs = paragraphs.filter(
            Q(sub_category=search_terms["as_subcat"]) | Q(regulation__sub_category=search_terms["as_subcat"])
        )
    if "as_reg" in search_terms.keys() and search_terms["as_reg"]:
        paragraphs = paragraphs.filter(regulation__regime=search_terms["as_reg"])
    if "as_type" in search_terms.keys() and search_terms["as_type"] and search_terms["as_type"] != "base":
        paragraphs = paragraphs.filter(note_type=search_terms["as_type"])
    return paragraphs
