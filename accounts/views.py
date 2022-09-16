from django.conf import settings
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["page_title"] = _("Profile")
        context["page_description"] = _("This is a test to see if the translations work")
        return context
