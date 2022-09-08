from django.db import models


class Regulation(models.Model):
    """
    A regulation is an item in the appendix of the Norwegian Export Control Law.

    It has:
    - a category (e.g. 4 - Navigation and Avionics)
    - a subcategory (e.g. A - Systems, Equipment and Components)
    - a regime (e.g. 001)

    ...which together form its identifier (e.g. 4A001).

    A regulation has text, which can be a single or multiple paragraphs, with notes and sub-paragraphs (points).
    """

    category = models.ForeignKey("Category")
    sub_category = models.ForeignKey("SubCategory")
    regime = models.ForeignKey("Regime")

    text = models.ManyToManyField("Paragraph")


class Category(models.Model):
    """
    A top-level category of regulations in the Norwegian Export Control Law.

    It has:
    - an identifier (e.g. 4)
    - a name (e.g. Navigation and Avionics)
    """

    identifier = models.IntegerField()
    name = models.CharField()


class SubCategory(models.Model):
    """
    A subcategory of regulations in the Norwegian Export Control Law.
    Every top-level category has regulations in every subcategory.

    It has:
    - an identifier (e.g. A)
    - a name (e.g. Systems, Equipment and Components)
    """

    identifier = models.CharField()
    name = models.CharField()


class Regime(models.Model):
    """
    A regime is the final category of a regulation in the Norwegian Export Control Law.

    It has:
    - an identifier (e.g. 001)
    """

    identifier = models.IntegerField()


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

    Paragraphs may also be notes, e.g.:
    ```
    1C232   Helium-3, mixtures containing helium-3, and products or devices containing any of the foregoing.
            Note: 1C232 does not control a product or device containing less than 1 g of helium-3.
    ```
    In this example, the `Note:` is its own `Paragraph`, with `note=True`.
    """

    text = models.TextField()
    parent = models.ForeignKey("Paragraph", null=True)
    note = models.BooleanField()
