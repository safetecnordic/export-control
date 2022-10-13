from django import forms
from django.utils.translation import gettext as _


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label=_("Search"),
    )
    category = forms.IntegerField(
        required=False,
        label=_("Category"),
    )
    subcategory = forms.IntegerField(
        required=False,
        label=_("SubCategory"),
    )
    regime = forms.IntegerField(
        required=False,
        label=_("Regime"),
    )
