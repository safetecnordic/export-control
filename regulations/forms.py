from django import forms
from django.utils.translation import gettext_lazy as _
from regulations.models import Category, Paragraph, SubCategory, Regime
from regulations.utils import get_formated_string


class SearchForm(forms.Form):

    as_q = forms.CharField(
        required=False,
        label=_("All these words:"),
    )
    as_qand = forms.CharField(
        required=False,
        label=_("This exact phrase:"),
    )
    as_qor = forms.CharField(
        required=False,
        label=_("Any of these words:"),
        help_text=_("(separated by space)"),
    )
    as_qnot = forms.CharField(
        required=False,
        label=_("None of these words:"),
        help_text=_("(separated by space)"),
    )
    as_cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label=_("Category:"),
    )
    as_subcat = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        label=_("Subcategory:"),
    )
    as_reg = forms.ModelChoiceField(
        queryset=Regime.objects.all(),
        required=False,
        label=_("Regime:"),
    )
    as_type = forms.ChoiceField(
        choices=(("", "---------"),) + Paragraph.NOTE_TYPE_CHOICES,
        required=False,
        label=_("Note type:"),
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
