from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from contacts.models import Contact


class ContactTests(TestCase):
    def test_add_contat_view(self):
        url = reverse("add_contact")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("Consult Safetec"))

        # test form
        contacts = Contact.objects.all()
        self.assertEqual(contacts.count(), 0)

        response = self.client.post(
            url,
            {
                "name": "",
                "email": "",
                "phone_number": "",
                "message": "",
            },
        )
        self.assertFormError(response, "form", "name", "This field is required.")
        self.assertFormError(response, "form", "email", "This field is required.")
        self.assertFormError(response, "form", "message", "This field is required.")

        contacts = Contact.objects.all()
        self.assertEqual(contacts.count(), 0)

        response = self.client.post(
            url,
            {
                "name": "Test",
                "email": "",
                "phone_number": "",
                "message": "",
            },
        )
        self.assertFormError(response, "form", "email", "This field is required.")
        self.assertFormError(response, "form", "message", "This field is required.")

        contacts = Contact.objects.all()
        self.assertEqual(contacts.count(), 0)
        response = self.client.post(
            url,
            {
                "name": "Test",
                "email": "test@test.come",
                "phone_number": "+39324587980",
                "message": "Add here some text",
            },
        )
        success_url = reverse("thank_you")
        self.assertRedirects(response, success_url)

        contacts = Contact.objects.all()
        contact = contacts.first()
        self.assertEqual(contacts.count(), 1)
        self.assertEqual(contact.message, "Add here some text")
        self.assertEqual(contact.name, "Test")
        self.assertEqual(contact.email, "test@test.come")
        self.assertEqual(contact.phone_number, "+39324587980")
