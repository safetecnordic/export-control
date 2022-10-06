from __future__ import annotations
import re
from django.db import models
from django.db.models import Q, F
from django.utils.translation import gettext as _
from django.db.models import Exists, OuterRef
from utils import types  # type: ignore
from ckeditor.fields import RichTextField
from treebeard.mp_tree import MP_Node


class Regulation(models.Model):
    """
    A regulation is an item in the appendix of the Norwegian Export Control Law.

    It has:
    - a `category` (e.g. 4 - Navigation and Avionics)
    - a `sub_category` (e.g. A - Systems, Equipment and Components)
    - a `regime` (e.g. Waasemaar Arrangement, which cover regime numbers 001 - 099)
    - a `regime_number` (e.g. 002, which is a number within the range covered by the Waasemaar Arrangement regime)

    The category, sub-category and regime number together form the regulation's identifier (e.g. 4A002).

    A regulation's text consists of `paragraphs`, connected through a foreign key from the `Paragraph` model below.
    """

    category: types.ForeignKey[Category] = models.ForeignKey("Category", on_delete=models.CASCADE)
    sub_category: types.ForeignKey[SubCategory] = models.ForeignKey("SubCategory", on_delete=models.CASCADE)
    regime: types.ForeignKey[Regime] = models.ForeignKey("Regime", on_delete=models.CASCADE)
    code: types.CharField = models.CharField(max_length=256, null=True, unique=True)

    date_created: types.DateTimeField = models.DateTimeField(_("Date created"), auto_now_add=True, db_index=True)
    date_updated: types.DateTimeField = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    def __str__(self) -> str:
        # regime_number:03d fills the string with leading zeros if the regime number is less than 3 digits.
        # e.g. 1 -> "001"
        return self.code

    def get_last_paragraph(self):
        return self.paragraphs.order_by("date_created").last()


class Category(models.Model):
    """
    A top-level category of regulations in the Norwegian Export Control Law.

    It has:
    - an `identifier` (e.g. 7)
    - a `name` (e.g. Navigation and Avionics)
    - an optional `part` (e.g. 1, for Category 5 Part 1: Telecommunications)
      - categories with parts are represented with one category per part in the database
      - the `name` of the category for each part is the name of the part (e.g. Telecommunications)
    """

    identifier: types.IntegerField = models.IntegerField()
    name: types.CharField = models.CharField(max_length=256)
    part: types.IntegerField = models.IntegerField(null=True, default=1)

    date_created: types.DateTimeField = models.DateTimeField(_("Date created"), auto_now_add=True, db_index=True)
    date_updated: types.DateTimeField = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    def __str__(self) -> str:
        part_str = f".{self.part}" if self.part is not None else ""
        return f"{self.identifier}{part_str}: {self.name}"


class SubCategory(models.Model):
    """
    A subcategory of regulations in the Norwegian Export Control Law.
    Every top-level category has regulations in every subcategory.

    It has:
    - an `identifier` (e.g. A)
    - a `name` (e.g. Systems, Equipment and Components)
    """

    identifier: types.CharField = models.CharField(max_length=256, unique=True)
    name: types.CharField = models.CharField(max_length=256)

    date_created: types.DateTimeField = models.DateTimeField(_("Date created"), auto_now_add=True, db_index=True)
    date_updated: types.DateTimeField = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    def __str__(self) -> str:
        return f"{self.identifier}: {self.name}"


class Regime(models.Model):
    """
    Each regulation in the Norwegian Export Control Law stems from a regime:
    an arrangement that Norway has entered into, which governs the control of certain products.

    For regulations in the law, each regime is assigned a number range to identify regulations covered by a regime.

    It has:
    - a `name` (e.g. Wassenaar Arrangement, which is a regime that covers arms exports)
    - a `number_range_min`, i.e. the start of this regime's number range (e.g. 1)
    - a `number_range_max`, i.e. the end of this regime's number range (e.g. 99)
    """

    name: types.CharField = models.CharField(max_length=256)
    number_range_min: types.IntegerField = models.IntegerField(unique=True)
    number_range_max: types.IntegerField = models.IntegerField(unique=True)

    date_created: types.DateTimeField = models.DateTimeField(_("Date created"), auto_now_add=True, db_index=True)
    date_updated: types.DateTimeField = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        # Enforces that number_range_min is less than number_range_max.
        constraints = [
            models.CheckConstraint(
                name="number_range_min_less_than_max", check=Q(number_range_min__lt=F("number_range_max"))
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class Paragraph(MP_Node):
    """
    A paragraph is a part of the text for a regulation in the Norwegian Export Control Law.

    Paragraphs can be nested under each other as sub-points, e.g.:
    ```
    2B231   Vacuum pumps having all of the following characteristics:
            a. Input throat size equal to or greater than 380 mm;
            b. Pumping speed equal to or greater than 15 m3
            c. Capable of producing an ultimate vacuum better than 13 mPa.
    ```
    In this example, each subpoint is its own `Paragraph`, with its `parent` set to the top sentence.

    Paragraphs have a zero-indexed `order` field for the order in which they should be displayed on their nesting level.
    In the example above, subpoint `a.` has `order=0`, subpoint `b.` has `order=1`, etc.

    Paragraphs may also be notes, e.g.:
    ```
    1C232   Helium-3, mixtures containing helium-3, and products or devices containing any of the foregoing.
            Note: 1C232 does not control a product or device containing less than 1 g of helium-3.
    ```
    In this example, has a special note_type.

    Paragraphs can either:
    - belong to a regulation (in which case `category` and `sub_category` are `NULL`)
    - belong to a category (in which case `regulation` and `sub_category` are `NULL`)
    - belong to a sub-category (in which case only `regulation` is `NULL`, since we must also specify category)
    """

    BASE, NOTE, NOTA_BENE, TECHNICAL_NOTE = (
        "base",
        "note",
        "nota_bene",
        "technical_note",
    )

    NOTE_TYPE_CHOICES = (
        (BASE, _("Base")),
        (NOTE, _("Note")),
        (NOTA_BENE, _("N.B.")),
        (TECHNICAL_NOTE, _("Technical Note")),
    )

    node_order_by = ["code"]

    code: types.CharField = models.CharField(max_length=256, default="-")
    note_type: types.CharField = models.CharField(
        max_length=256,
        choices=NOTE_TYPE_CHOICES,
        default=BASE,
    )

    text: types.RichTextField = RichTextField(blank=False)
    is_public: types.BooleanField = models.BooleanField(default=True)

    regulation: types.ForeignKey[Regulation] = models.ForeignKey(
        "Regulation", null=True, on_delete=models.CASCADE, related_name="paragraphs"
    )
    category: types.ForeignKey[Category] = models.ForeignKey(
        "Category", null=True, on_delete=models.CASCADE, related_name="paragraphs"
    )
    sub_category: types.ForeignKey[SubCategory] = models.ForeignKey(
        "SubCategory", null=True, on_delete=models.CASCADE, related_name="paragraphs"
    )

    date_created: types.DateTimeField = models.DateTimeField(_("Date created"), auto_now_add=True, db_index=True)
    date_updated: types.DateTimeField = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    _full_name_separator = " > "

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        codes = [paragraph.code for paragraph in self.get_ancestors_and_self()]
        return "".join(codes)

    def set_ancestors_are_public(self):
        included_in_non_public_subtree = self.__class__.objects.filter(
            is_public=False, path__rstartswith=OuterRef("path"), depth__lt=OuterRef("depth")
        )
        self.get_descendants_and_self().update(
            ancestors_are_public=Exists(included_in_non_public_subtree.values("id"), negated=True)
        )
        self.refresh_from_db()

    @classmethod
    def fix_tree(cls, destructive=False):
        super().fix_tree(destructive)
        for node in cls.get_root_nodes():
            if not node.ancestors_are_public:
                node.ancestors_are_public = True
                node.save()
            else:
                node.set_ancestors_are_public()

    def get_ancestors_and_self(self):
        """
        :returns: A queryset containing the current paragraph's ancestors, \
            starting by the root paragraph and descending to the paragraph, and the paragraph itself.
        """
        if self.is_root():
            return [self]
        return list(self.get_ancestors()) + [self]

    def get_descendants_and_self(self):
        """
        :returns: A queryset of descendant paragraphs ordered as DFS, including the paragraph itself.
        """
        return self.get_tree(self)

    def is_special(self):
        """
        :returns: True if the paragraph is Note, N.B. or Technical Note, False otherwise.
        """
        return self.note_type != self.BASE
