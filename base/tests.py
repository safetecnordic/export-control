from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from django.utils.translation import gettext as _
from base.models import ExtendedFlatPage


class BaseTests(TestCase):
    def test_front_page_view(self):
        url = reverse("front_page")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Safetec"))
        self.assertContains(response, _("Search"))
        self.assertContains(response, _("Consult Safetec"))

    def test_flatpage_front_page_view(self):
        url = reverse("front_page")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ExtendedFlatPage.objects.filter(url="/home/").exists())
        page = ExtendedFlatPage.objects.get(url="/home/")
        page.title = "Home Page Site ING"
        page.save()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home Page Site ING")
        activate("no")
        url = reverse("front_page")
        page.title_no = "Home Page Site NO"
        page.save()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home Page Site NO")

    def test_flatpages(self):
        site = Site.objects.get(id=1)
        url_title = "/export-control-law/"
        url = reverse("django.contrib.flatpages.views.flatpage", kwargs={"url": url_title})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(ExtendedFlatPage.objects.filter(url=url).exists())
        page, new = ExtendedFlatPage.objects.get_or_create(
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
        url = reverse("django.contrib.flatpages.views.flatpage", kwargs={"url": url_title})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ExportControl Law")
        self.assertContains(response, "BODY TEST")
        self.assertContains(response, "ENG")

        activate("no")
        url = reverse("django.contrib.flatpages.views.flatpage", kwargs={"url": url_title})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ExportControl Law")
        self.assertContains(response, "BODY TEST")
        self.assertContains(response, "NO")
