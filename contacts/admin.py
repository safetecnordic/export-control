from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = (
        "name",
        "email",
        "phone_number",
        "message",
        "date_created",
        "status",
        "archived",
    )
    list_filter = (
        "status",
        "archived",
    )
    search_fields = ("name", "email", "phone_number")


admin.site.register(Contact, ContactAdmin)
