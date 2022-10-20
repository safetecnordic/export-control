from django.test import TestCase

from regulations.models import Paragraph
from regulations.search import get_searched_paragraphs


class SearchTests(TestCase):
    fixtures = [
        "init_paragraphs",
    ]

    def test_get_searched_paragraphs(self):
        paragraphs = get_searched_paragraphs("URANIUM")
        self.assertEqual(paragraphs.count(), 5)
        paragraphs = get_searched_paragraphs("uraANIum")
        self.assertEqual(paragraphs.count(), 5)
        paragraphs = get_searched_paragraphs("******uraANIum**********")
        self.assertEqual(paragraphs.count(), 0)
        paragraphs = get_searched_paragraphs("uranium")
        self.assertEqual(paragraphs.count(), 5)
        paragraphs = get_searched_paragraphs("hydrogen")
        self.assertEqual(paragraphs.count(), 5)
        paragraphs = get_searched_paragraphs("hydrogen uranium")
        self.assertEqual(paragraphs.count(), 5)
        paragraphs = get_searched_paragraphs("uranium hydrogen")
        self.assertEqual(paragraphs.count(), 5)
        paragraphs = get_searched_paragraphs("Magnesium")
        self.assertEqual(paragraphs.count(), 2)
