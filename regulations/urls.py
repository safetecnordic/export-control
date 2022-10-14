from django.urls import path
from regulations.models import Regulation
from regulations.views import SearchView, RegulationDetailView

urlpatterns = [
    path("search", SearchView.as_view(), name="search"),
    path("<str:code>", RegulationDetailView.as_view(), name="regulation_detail"),
]
