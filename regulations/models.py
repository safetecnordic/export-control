from django.db import models
from utils import types  # type: ignore


class Regulation(models.Model):
    """
    A regulation is an item in the appendix of the Norwegian Export Control Law.

    It has:
    - a `category` (e.g. 4 - Navigation and Avionics)
    - a `sub_category` (e.g. A - Systems, Equipment and Components)
    - a `regime` (e.g. 001)

    ...which together form its identifier (e.g. 4A001).

    A regulation's text consists of `paragraphs`, connected through a foreign key from the `Paragraph` model below.
    """

    category: types.ForeignKey["Category"] = models.ForeignKey("Category", on_delete=models.CASCADE)
    sub_category: types.ForeignKey["SubCategory"] = models.ForeignKey("SubCategory", on_delete=models.CASCADE)
    regime: types.ForeignKey["Regime"] = models.ForeignKey("Regime", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.category.identifier}{self.sub_category.identifier}{self.regime.identifier}"


class Category(models.Model):
    """
    A top-level category of regulations in the Norwegian Export Control Law.

    It has:
    - an identifier (e.g. 4)
    - a name (e.g. Navigation and Avionics)
    """

    identifier: types.IntegerField = models.IntegerField()
    name: types.CharField = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.identifier}: {self.name}"


class SubCategory(models.Model):
    """
    A subcategory of regulations in the Norwegian Export Control Law.
    Every top-level category has regulations in every subcategory.

    It has:
    - an identifier (e.g. A)
    - a name (e.g. Systems, Equipment and Components)
    """

    identifier: types.CharField = models.CharField(max_length=256)
    name: types.CharField = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.identifier}: {self.name}"


class Regime(models.Model):
    """
    A regime is the final category of a regulation in the Norwegian Export Control Law.

    It has:
    - an identifier (e.g. 001)
    """

    identifier: types.CharField = models.CharField(max_length=3)

    def __str__(self) -> str:
        return f"{self.identifier}"


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
    """

    regulation: types.ForeignKey[Regulation] = models.ForeignKey(
        "Regulation", on_delete=models.CASCADE, related_name="paragraphs"
    )

    text: types.TextField = models.TextField(blank=False)
    order: types.IntegerField = models.IntegerField(unique=True)
    note: types.BooleanField = models.BooleanField(default=False)
    parent: types.ForeignKey["Paragraph"] = models.ForeignKey("Paragraph", null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        s = f"Paragraph {self.order} of {self.regulation.__str__()}"

        if self.parent is not None:
            s += f" (child of {self.parent.__str__()})"

        return s

    # inserire related name = children
