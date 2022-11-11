from django.db import models
from django.utils.safestring import mark_safe
from utils import types
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    # STATUS_CHOICES
    NEW, IN_PROGRESS, RESOLVED, CANCELED = (
        "new",
        "in_progress",
        "resolved",
        "canceled",
    )
    STATUS_CHOICES = (
        (NEW, "New"),
        (IN_PROGRESS, "In progress"),
        (RESOLVED, "Resolved"),
        (CANCELED, "Cancelled"),
    )

    name: types.CharField = models.CharField(max_length=128)

    email: types.CharField = models.EmailField()

    phone_number = PhoneNumberField(null=True, blank=True)

    message: types.TextField = models.TextField()

    status: types.CharField = models.CharField(choices=STATUS_CHOICES, max_length=30, default=NEW)

    archived: types.BooleanField = models.BooleanField(default=False)

    date_created: types.DateTimeField = models.DateTimeField(auto_now_add=True, db_index=True)

    date_updated: types.DateTimeField = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.name

    def get_status_display_in_admin(self):
        text = ""
        if self.status:
            status_class = ""
            if self.status == self.NEW:
                status_class = "info"
            elif self.status == self.IN_PROGRESS:
                status_class = "secondary"
            elif self.status == self.CANCELED:
                status_class = "danger"
            elif self.status == self.RESOLVED:
                status_class = "success"
            text = mark_safe(
                f"<div class='badge bg-{status_class}' title='{self.status.title()}' style='min-width: 65px; display:inline-block;'>{self.status.title()}</div>"
            )
        return text

    get_status_display_in_admin.short_description = "Status"  # type: ignore
