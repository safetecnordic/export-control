from django import forms
from django.utils.translation import gettext as _
from regulations.models import Category, Paragraph, Regulation, SubCategory, Regime


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label=_("Category"),
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        label=_("SubCategory"),
    )
    regime = forms.ModelChoiceField(
        queryset=Regime.objects.all(),
        required=False,
        label=_("Regime"),
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["q"].label = ""
