from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from regulations.forms import SearchForm
from regulations.search import SearchQueries, filter_paragraphs
from regulations.utils import get_formated_string, set_postgres_search_config
from regulations.models import Category, SubCategory, Regime, Paragraph


class SearchTests(TestCase):
    fixtures = [
        "test_data",
    ]

    def setUp(self):
        self.paragraphs = Paragraph.objects.all()
        set_postgres_search_config()

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

    def test_paragraph_search(self):
        # CHECK "QUERY"
        queries = SearchQueries({"as_q": "URANIUM"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_q": "urANIum"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_q": "uranium"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_q": "hydrogen"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_q": "hydrogen uranium"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({"as_q": "uranium hydrogen"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({"as_q": "Magnesium"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 4)

        queries = SearchQueries({"as_q": "django"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "only"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        queries = SearchQueries({"as_q": "only django"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "uranium hydrogenTest"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        # CHECK "NOT QUERY"
        queries = SearchQueries({"as_q": "uranium hydrogen", "as_qnot": "hydrogen"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        queries = SearchQueries({"as_q": "uranium hydrogen", "as_qnot": "uranium"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        queries = SearchQueries({"as_q": "uranium", "as_qnot": "hydrogen"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        queries = SearchQueries({"as_q": "hydrogen", "as_qnot": "uranium"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        queries = SearchQueries({"as_q": "uranium", "as_qnot": "words"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        queries = SearchQueries({"as_q": "uranium", "as_qnot": "('TEST' OR 'django')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 4)

        queries = SearchQueries({"as_q": "hydrogen", "as_qnot": "('magnesium')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({"as_q": "uranium", "as_qnot": "('TEST' OR 'django' OR 'magnesium')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        # CHECK "AND QUERY"
        queries = SearchQueries({"as_q": "word"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_q": "words"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_q": "words", "as_qand": "uranium"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({"as_q": "words", "as_qand": "hydrogen"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({"as_q": "hydrogen", "as_qand": "uranium and"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "hydrogen", "as_qand": "uranium and hydrogen"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "hydrogen", "as_qand": "uranium hydrogen"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "words", "as_qand": "This field"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({"as_q": "words", "as_qand": "TEST field"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "words", "as_qand": "field contains"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 6)

        queries = SearchQueries({"as_q": "words", "as_qand": "field contains TEST"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "words", "as_qand": "field contains the"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 3)

        queries = SearchQueries({"as_q": "words", "as_qand": "This field contains the"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        queries = SearchQueries({"as_q": "words", "as_qand": "This field contains TEST"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "words", "as_qand": "TEST field contains the"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_q": "words", "as_qand": "TEST field contains TEST"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        # CHECK "OR QUERY"
        queries = SearchQueries({"as_q": "words", "as_qor": "Magnesium"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 3)

        queries = SearchQueries({"as_q": "word", "as_qor": "Magnesium"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 3)

        queries = SearchQueries({"as_q": "words", "as_qor": "hydrogen"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({"as_q": "words", "as_qor": "('hydrogen' OR 'Magnesium')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_qor": "('hydrogen' OR 'Magnesium')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 9)

        queries = SearchQueries({"as_q": "TEST", "as_qor": "('hydrogen' OR 'Magnesium')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        queries = SearchQueries({"as_qor": "('word')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_qor": "('words')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        queries = SearchQueries({"as_qor": "('words' OR 'word')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 7)

        # CHECK "AND QUERY" & "NOT QUERY"
        queries = SearchQueries({"as_q": "hydrogen", "as_qand": "This field"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 4)

        queries = SearchQueries({"as_q": "hydrogen", "as_qand": "This field contains"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 4)

        queries = SearchQueries({"as_q": "hydrogen", "as_qand": "This field contain"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 4)

        queries = SearchQueries({"as_q": "hydrogen", "as_qand": "This field", "as_qnot": "contain"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        queries = SearchQueries({"as_q": "hydrogen", "as_qand": "This field", "as_qnot": "('contain' OR 'test')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        # CHECK "AND QUERY" & "OR QUERY" & "NOT QUERY"
        queries = SearchQueries({
            "as_q": "hydrogen",
            "as_qand": "This field",
            "as_qnot": "('test')",
            "as_qor": "('magnesium')",
        })
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        p = paragraphs.first()
        self.assertEqual(paragraphs.count(), 1)

        self.assertTrue("hydrogen" in p.text)
        self.assertTrue("This field" in p.text)
        self.assertTrue("magnesium" in p.text)
        self.assertFalse("test" in p.text)

        queries = SearchQueries({
            "as_q": "hydrogen",
            "as_qand": "This field",
            "as_qnot": "('words' OR 'test')",
            "as_qor": "('magnesium')",
        })
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        p = paragraphs.first()
        self.assertEqual(paragraphs.count(), 0)

    def test_stop_words_database(self):
        queries = SearchQueries({"as_q": "message"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 3)

        queries = SearchQueries({"as_q": "nuclear"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 3)

        queries = SearchQueries({"as_q": "nuclears"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 3)

        queries = SearchQueries({"as_q": "exportcontrol", "as_qor": "('message_wrong' OR 'nuclears')"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        queries = SearchQueries({"as_q": "exportcontrol", "as_qor": "('message_wrong' OR 'nuclears')", "as_and": "and"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 2)

        queries = SearchQueries({"as_q": "exportcontrol", "as_qnot": "message"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        queries = SearchQueries({"as_q": "exportcontrol", "as_qnot": "message_wrong"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_qor": "message", "as_qand": "nuclears and exportcontrol"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_qor": "message", "as_qand": "nuclears exportcontrol"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_qor": "message", "as_qand": "nuclear exportcontrol"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 1)

        queries = SearchQueries({"as_qor": "message", "as_qand": "nuclear test exportcontrol"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        queries = SearchQueries({"as_qor": "message", "as_qand": "nuclear_test exportcontrol"})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

    def test_category_filters(self):
        # pk: 0 = Category: 0
        queries = SearchQueries({"as_cat": Category.objects.get(identifier=0), "as_type": Paragraph.BASE})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 10)

        queries = SearchQueries({"as_cat": Category.objects.get(identifier=1), "as_type": Paragraph.BASE})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

        queries = SearchQueries({"as_subcat": SubCategory.objects.get(identifier="A"), "as_type": Paragraph.BASE})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({"as_subcat": SubCategory.objects.get(identifier="B"), "as_type": Paragraph.BASE})
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({
            "as_cat": Category.objects.get(identifier=0),
            "as_subcat": SubCategory.objects.get(identifier="A"),
            "as_type": Paragraph.BASE,
        })
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({
            "as_cat": Category.objects.get(identifier=0),
            "as_subcat": SubCategory.objects.get(identifier="A"),
            "as_reg": Regime.objects.get(pk=1),
            "as_type": Paragraph.BASE,
        })
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 5)

        queries = SearchQueries({
            "as_cat": Category.objects.get(identifier=0),
            "as_subcat": SubCategory.objects.get(identifier="A"),
            "as_reg": Regime.objects.get(pk=2),
            "as_type": Paragraph.BASE,
        })
        paragraphs = filter_paragraphs(self.paragraphs, queries)
        self.assertEqual(paragraphs.count(), 0)

    def test_is_public_paragraphs(self):
        queries = SearchQueries({"as_cat": Category.objects.get(identifier=0), "as_type": Paragraph.BASE})
        paragraphs = filter_paragraphs(self.paragraphs, queries).filter(is_public=True)
        self.assertEqual(paragraphs.count(), 10)

        p = paragraphs.get(code="0A001")
        p.is_public = False
        p.save()

        queries = SearchQueries({"as_cat": Category.objects.get(identifier=0), "as_type": Paragraph.BASE})
        paragraphs = filter_paragraphs(self.paragraphs, queries).filter(is_public=True)
        self.assertEqual(paragraphs.count(), 9)
