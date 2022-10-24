from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from contatcs.models import Contact


class ContactTests(TestCase):
    def test_search_view(self):
        url = reverse("contact_add")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Consult Safetec"))

    """    def test_search_form(self):
        form_data = {"as_q": "Hydrogen", "as_cat": "TEST"}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["as_cat"][0], "Select a valid choice. That choice is not one of the available choices."
        )
        form_data = {"as_q": "Hydrogen", "as_cat": 1}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())"""
