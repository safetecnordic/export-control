from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _


class BaseTests(TestCase):
    def test_front_page_view(self):
        url = reverse("front_page")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Safetec"))
        self.assertContains(response, _("Search"))
        self.assertContains(response, _("Consult Safetec"))
