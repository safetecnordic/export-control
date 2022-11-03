from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = (
        "name",
        "email",
        "phone_number",
        "date_created",
        "get_status_display_in_admin",
        "archived",
    )
    list_filter = (
        "status",
        "archived",
    )
    actions = [
        "set_archived",
    ]
    search_fields = ("name", "email", "phone_number")

    def set_archived(self, request, queryset):
        if not self.has_change_permission(request):
            raise PermissionDenied
        Contact.objects.filter(pk__in=queryset.values_list("pk", flat=True)).update(archived=True)
        self.message_user(request, "The contacts has been updated")


admin.site.register(Contact, ContactAdmin)
