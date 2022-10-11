from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = (
        "name",
        "email",
        "phone",
        "message",
        "date_created",
    )
    list_filter = ("name", "email", "phone")
    search_fields = ("name", "email")

admin.site.register(Contact, ContactAdmin)