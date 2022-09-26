from __future__ import annotations
from django.db import models
from django.db.models import Q, F
from utils import types  # type: ignore


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
    regime_number: types.IntegerField = models.IntegerField()

    def __str__(self) -> str:
        # regime_number:03d fills the string with leading zeros if the regime number is less than 3 digits.
        # e.g. 1 -> "001"
        return f"{self.category.identifier}{self.sub_category.identifier}{self.regime_number:03d}"


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
    part: types.IntegerField = models.IntegerField(null=True, default=None)

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

    class Meta:
        # Enforces that number_range_min is less than number_range_max.
        constraints = [
            models.CheckConstraint(
                name="number_range_min_less_than_max", check=Q(number_range_min__lt=F("number_range_max"))
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class Paragraph(models.Model):
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
    In this example, the `Note:` is its own `Paragraph`, with `note=True`.

    Paragraphs can either:
    - belong to a regulation (in which case `category` and `sub_category` are `NULL`)
    - belong to a category (in which case `regulation` and `sub_category` are `NULL`)
    - belong to a sub-category (in which case only `regulation` is `NULL`, since we must also specify category)
    """

    text: types.TextField = models.TextField(blank=False)
    order: types.IntegerField = models.IntegerField(unique=True)
    note: types.BooleanField = models.BooleanField(default=False)
    parent: types.ForeignKey[Paragraph] = models.ForeignKey("Paragraph", null=True, on_delete=models.CASCADE)

    regulation: types.ForeignKey[Regulation] = models.ForeignKey(
        "Regulation", null=True, on_delete=models.CASCADE, related_name="paragraphs"
    )
    category: types.ForeignKey[Category] = models.ForeignKey(
        "Category", null=True, on_delete=models.CASCADE, related_name="paragraphs"
    )
    sub_category: types.ForeignKey[SubCategory] = models.ForeignKey(
        "SubCategory", null=True, on_delete=models.CASCADE, related_name="paragraphs"
    )

    class Meta:
        constraints = [
            # Enforces that a paragraph belongs to an appropriate parent, as described in the Paragraph docstring above.
            models.CheckConstraint(
                name="valid_parent",
                check=(
                    (Q(regulation__isnull=False) & Q(category__isnull=True) & Q(sub_category__isnull=True))
                    | (Q(regulation__isnull=True) & Q(category__isnull=False))
                ),
            )
        ]

    def __str__(self) -> str:
        s = f"Paragraph {self.order} of {self.regulation.__str__()}"

        if self.parent is not None:
            s += f" (child of {self.parent.__str__()})"

        return s

    # inserire related name = children
