from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
from regulations.models import Category, Paragraph, SubCategory, Regime
#TemplateView should be used when you want to present some information on an HTML page. TemplateView shouldn’t 
#be used when your page has forms and does creation or update of objects. In such cases, 
#FormView, CreateView, or UpdateView is a better option.
def search(request):    
    q = request.GET.get('q')
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    regimes = Regime.objects.all()
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    regime_id = request.GET.get('regime')
    
    paragraphs = None

    if q:
        vector = SearchVector('text')
        query = SearchQuery(q)
        search_headline = SearchHeadline('text', query) 
        paragraphs = Paragraph.objects. \
            annotate(rank = SearchRank(vector, query)).annotate(headline = search_headline).filter(rank__gte=0.001).order_by('-rank')
    else:
        # if query string is empty return only parent nodes
        paragraphs = Paragraph.get_root_nodes()

    if category_id:
        paragraphs = paragraphs.filter(regulation__category__id = int(category_id))
    if subcategory_id:
        paragraphs = paragraphs.filter(regulation__sub_category__id = int(subcategory_id))
    if regime_id:
        paragraphs = paragraphs.filter(regulation__regime__id = int(regime_id))
        
    if paragraphs:
        paginator = Paginator(paragraphs, 10)
        page = request.GET.get('page')
        paged_paragraphs = paginator.get_page(page)
    else:
        paged_paragraphs = None
    context = dict()
    context["page_title"] = settings.SITE_NAME
    context["page_description"] = _("This is a test to see if the translations work")
    context["categories"] = categories
    context["subcategories"] = subcategories
    context["regimes"] = regimes
    context['paragraphs'] = paged_paragraphs
    context['q'] = q
    category = Category.objects.get(id = category_id) if category_id else None
    context['category'] = category
    subcategory = SubCategory.objects.get(id = subcategory_id) if subcategory_id else None
    context['subcategory'] = subcategory
    regime = Regime.objects.get(id = regime_id) if regime_id else None
    context['regime'] = regime
    return render(request, "base/presentation.html", context)



