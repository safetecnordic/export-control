from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from regulations.forms import SearchForm
from regulations.search import get_searched_paragraphs, get_filtered_paragraphs
from regulations.utils import get_formated_string
from regulations.models import Category, SubCategory, Regime, Paragraph


class SearchTests(TestCase):
    fixtures = [
        "init_data",
    ]

    def setUp(self):
        self.paragraphs = Paragraph.objects.all()

    def test_get_formated_string(self):
        self.assertEqual(get_formated_string("", "OR"), "()")
        self.assertEqual(get_formated_string("1", "OR"), "('1')")
        self.assertEqual(get_formated_string("1test1", "OR"), "('1test1')")
        self.assertEqual(get_formated_string("test", "OR"), "('test')")
        self.assertEqual(get_formated_string("test exportcontrol", "OR"), "('test' OR 'exportcontrol')")
        self.assertEqual(
            get_formated_string("test exportcontrol email", "OR"), "('test' OR 'exportcontrol' OR 'email')"
        )
        self.assertEqual(get_formated_string("test exportcontrol", "AND"), "('test' AND 'exportcontrol')")

    def test_search_view(self):
        url = reverse("search")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Search"))
        self.assertContains(response, _("Advanced Search"))

    def test_search_form(self):
        form_data = {"as_q": "Hydrogen", "as_cat": "TEST"}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["as_cat"][0], "Select a valid choice. That choice is not one of the available choices."
        )
        form_data = {"as_q": "Hydrogen", "as_cat": 1}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_get_searched_paragraphs(self):
        # CHECK "QUERY"
        input_values = {"as_q": "URANIUM"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 7)
        input_values = {"as_q": "urANIum"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 7)
        input_values = {"as_q": "uranium"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 7)
        input_values = {"as_q": "hydrogen"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 7)
        input_values = {"as_q": "hydrogen uranium"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)
        input_values = {"as_q": "uranium hydrogen"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)
        input_values = {"as_q": "Magnesium"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 4)
        input_values = {"as_q": "django"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "only"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)
        input_values = {"as_q": "only django"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "uranium hydrogenTest"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 0)

        # CHECK "NOT QUERY"
        input_values = {"as_q": "uranium hydrogen", "as_qnot": "hydrogen"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 0)
        input_values = {"as_q": "uranium hydrogen", "as_qnot": "uranium"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 0)
        input_values = {"as_q": "uranium", "as_qnot": "hydrogen"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)
        input_values = {"as_q": "hydrogen", "as_qnot": "uranium"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)
        input_values = {"as_q": "uranium", "as_qnot": "words"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)
        input_values = {"as_q": "uranium", "as_qnot": "('TEST' OR 'django')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 4)
        input_values = {"as_q": "hydrogen", "as_qnot": "('magnesium')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)
        input_values = {"as_q": "uranium", "as_qnot": "('TEST' OR 'django' OR 'magnesium')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)

        # CHECK "AND QUERY"
        input_values = {"as_q": "words"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 6)
        input_values = {"as_q": "words", "as_qand": "uranium"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)
        input_values = {"as_q": "words", "as_qand": "hydrogen"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)
        input_values = {"as_q": "hydrogen", "as_qand": "uranium and"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "hydrogen", "as_qand": "uranium and hydrogen"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "hydrogen", "as_qand": "uranium hydrogen"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "words", "as_qand": "This field"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)
        input_values = {"as_q": "words", "as_qand": "TEST field"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "words", "as_qand": "field contains"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 4)
        input_values = {"as_q": "words", "as_qand": "field contains TEST"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "words", "as_qand": "field contains the"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 3)
        input_values = {"as_q": "words", "as_qand": "This field contains the"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)
        input_values = {"as_q": "words", "as_qand": "This field contains TEST"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "words", "as_qand": "TEST field contains the"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "words", "as_qand": "TEST field contains TEST"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 0)

        # CHECK "OR QUERY"
        input_values = {"as_q": "words", "as_qor": "Magnesium"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)
        input_values = {"as_q": "words", "as_qor": "hydrogen"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)
        input_values = {"as_q": "words", "as_qor": "('hydrogen' OR 'Magnesium')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 6)
        input_values = {"as_qor": "('hydrogen' OR 'Magnesium')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 9)
        input_values = {"as_q": "TEST", "as_qor": "('hydrogen' OR 'Magnesium')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)
        input_values = {"as_qor": "('word')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_qor": "('words')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 6)
        input_values = {"as_qor": "('words' OR 'word')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 7)

        # CHECK "AND QUERY" & "NOT QUERY"
        input_values = {"as_q": "hydrogen", "as_qand": "This field"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 4)
        input_values = {"as_q": "hydrogen", "as_qand": "This field contains"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 3)
        input_values = {"as_q": "hydrogen", "as_qand": "This field contain"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 1)
        input_values = {"as_q": "hydrogen", "as_qand": "This field", "as_qnot": "contain"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 3)
        input_values = {"as_q": "hydrogen", "as_qand": "This field", "as_qnot": "('contain' OR 'test')"}
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 2)

        # CHECK "AND QUERY" & "OR QUERY" & "NOT QUERY"
        input_values = {
            "as_q": "hydrogen",
            "as_qand": "This field",
            "as_qnot": "('test')",
            "as_qor": "('magnesium')",
        }
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        p = paragraphs.first()
        self.assertEqual(paragraphs.count(), 1)

        self.assertTrue("hydrogen" in p.text)
        self.assertTrue("This field" in p.text)
        self.assertTrue("magnesium" in p.text)
        self.assertFalse("test" in p.text)

        input_values = {
            "as_q": "hydrogen",
            "as_qand": "This field",
            "as_qnot": "('words' OR 'test')",
            "as_qor": "('magnesium')",
        }
        paragraphs = get_searched_paragraphs(input_values, self.paragraphs)
        p = paragraphs.first()
        self.assertEqual(paragraphs.count(), 0)

    def test_get_filtered_paragraphs(self):
        input_values = {"as_cat": Category.objects.get(identifier=0), "as_type": Paragraph.BASE}  # pk: 0 = Category: 0
        paragraphs = get_filtered_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 10)

        input_values = {"as_cat": Category.objects.get(identifier=1), "as_type": Paragraph.BASE}
        paragraphs = get_filtered_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 0)

        input_values = {"as_subcat": SubCategory.objects.get(identifier="A"), "as_type": Paragraph.BASE}
        paragraphs = get_filtered_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)

        input_values = {"as_subcat": SubCategory.objects.get(identifier="B"), "as_type": Paragraph.BASE}
        paragraphs = get_filtered_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)

        input_values = {
            "as_cat": Category.objects.get(identifier=0),
            "as_subcat": SubCategory.objects.get(identifier="A"),
            "as_type": Paragraph.BASE,
        }
        paragraphs = get_filtered_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)

        input_values = {
            "as_cat": Category.objects.get(identifier=0),
            "as_subcat": SubCategory.objects.get(identifier="A"),
            "as_reg": Regime.objects.get(pk=1),
            "as_type": Paragraph.BASE,
        }
        paragraphs = get_filtered_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 5)

        input_values = {
            "as_cat": Category.objects.get(identifier=0),
            "as_subcat": SubCategory.objects.get(identifier="A"),
            "as_reg": Regime.objects.get(pk=2),
            "as_type": Paragraph.BASE,
        }
        paragraphs = get_filtered_paragraphs(input_values, self.paragraphs)
        self.assertEqual(paragraphs.count(), 0)
