from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from regulations.models import Category, Paragraph, SubCategory, Regime
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
#TemplateView should be used when you want to present some information on an HTML page. TemplateView shouldn’t 
#be used when your page has forms and does creation or update of objects. In such cases, 
#FormView, CreateView, or UpdateView is a better option.
def search(request):    
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    regimes = Regime.objects.all()
    q = request.GET.get('q')
    if q:
        vector = SearchVector('text')
        query = SearchQuery(q)
        search_headline = SearchHeadline('text', query) 
        paragraphs = Paragraph.objects. \
            annotate(rank = SearchRank(vector, query)).annotate(headline = search_headline).filter(rank__gte=0.001).order_by('-rank')
    else:
        paragraphs = None
    context = dict()
    context["page_title"] = settings.SITE_NAME
    context["page_description"] = _("This is a test to see if the translations work")
    context["categories"] = categories
    context["subcategories"] = subcategories
    context["regimes"] = regimes
    context['paragraphs'] = paragraphs
    context['q'] = q
    return render(request, "base/presentation.html", context)



