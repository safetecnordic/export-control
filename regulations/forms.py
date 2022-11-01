from django import forms
from django.utils.translation import gettext_lazy as _
from regulations.models import Category, Paragraph, SubCategory, Regime
from regulations.utils import get_formated_string


class SearchForm(forms.Form):

    as_q = forms.CharField(
        required=False,
        label=_("all these words:"),
        help_text=_("Type in the important words: <b>Chemical Heat Molecular</b>"),
    )
    as_qand = forms.CharField(
        required=False,
        label=_("this exact phrase:"),
        help_text=_("Type the exact phrase: <b>High Stability</b>"),
    )
    as_qor = forms.CharField(
        required=False,
        label=_("any of these words:"),
        help_text=_("Type all the words you want to include, separated by space: <b>Thumbnail Standard </b>"),
    )
    as_qnot = forms.CharField(
        required=False,
        label=_("none of these words:"),
        help_text=_("Type all words you want to exclude, separated by space: <b>nuclear</b>"),
    )
    as_cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label=_("category:"),
        help_text=_("Filter by <b>Category</b>"),
    )
    as_subcat = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        label=_("sub category:"),
        help_text=_("Filter by <b>Sub Category</b>"),
    )
    as_reg = forms.ModelChoiceField(
        queryset=Regime.objects.all(),
        required=False,
        label=_("regime:"),
        help_text=_("Filter by <b>Regime</b>"),
    )
    as_type = forms.ChoiceField(
        choices=Paragraph.NOTE_TYPE_CHOICES,
        required=False,
        label=_("type:"),
        help_text=_("Filter by Note Type: <b>BASE, N.B., Technical Note,  Note</b>"),
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

    def clean_as_type(self):
        note_type = self.cleaned_data["as_type"]
        if note_type:
            if note_type in [val[0] for val in Paragraph.NOTE_TYPE_CHOICES]:
                return note_type
            raise forms.ValidationError(_("Incorrect value entered."))
        return Paragraph.BASE

    def clean_as_qor(self):
        if self.cleaned_data["as_qor"]:
            return get_formated_string(self.cleaned_data["as_qor"], "OR")

    def clean_as_qnot(self):
        if self.cleaned_data["as_qnot"]:
            return get_formated_string(self.cleaned_data["as_qnot"], "OR")
