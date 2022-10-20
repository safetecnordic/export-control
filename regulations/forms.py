from django import forms
from django.utils.translation import gettext as _
from regulations.models import Category, Paragraph, Regulation, SubCategory, Regime


class SearchForm(forms.Form):

    as_q = forms.CharField(
        required=False,
        label=_("all these words:"),
        help_text=_("Type in the important words: <b>Chemical Heat Molecular</b>"),
    )
    as_ewq = forms.CharField(
        required=False,
        label=_("this exact word or phrase:"),
        help_text=_('Enclose the exact words in quotation marks: <b>"High stability"</b>'),
    )
    as_orq = forms.CharField(
        required=False,
        label=_("any of these words:"),
        help_text=_("Type OR between as many words as you want:  <b>thumbnail OR standard </b>"),
    )
    as_nwq = forms.CharField(
        required=False,
        label=_("none of these words:"),
        help_text=_("Antepone the - (minus) sign to the words to be excluded:  <b>-nuclear</b>"),
    )
    as_cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label=_("category:"),
        help_text=_("Filter by category"),
    )
    as_subcat = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        label=_("sub category:"),
        help_text=_("Filter by sub category"),
    )
    as_reg = forms.ModelChoiceField(
        queryset=Regime.objects.all(),
        required=False,
        label=_("regime:"),
        help_text=_("Filter by regime"),
    )
    as_type = forms.ChoiceField(
        choices=Paragraph.NOTE_TYPE_CHOICES,
        required=False,
        label=_("type:"),
        help_text=_("Filter by type"),
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
