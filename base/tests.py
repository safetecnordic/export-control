from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from base.models import ExtendedFlatPage


class BaseTests(TestCase):
    def test_flatpages(self):
        site = Site.objects.get(id=1)
        url_title = "/about/"
        url = reverse("about")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(ExtendedFlatPage.objects.filter(url=url).exists())
        page, created = ExtendedFlatPage.objects.get_or_create(
            url=url,
            title="ExportControl Law ENG",
            title_no="ExportControl Law NO",
            page_content="ExportControl Law BODY TEST ENG",
            page_content_no="ExportControl Law BODY TEST NO",
            template_name="flatpages/default.html",
        )
        self.assertTrue(ExtendedFlatPage.objects.filter(url=url).exists())
        page.sites.add(site)
        page.save()
        url = reverse("about")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ExportControl Law")
        self.assertContains(response, "BODY TEST")
        self.assertContains(response, "ENG")

        activate("no")
        url = reverse("about")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ExportControl Law")
        self.assertContains(response, "BODY TEST")
        self.assertContains(response, "NO")
