from django.db import models
from django.utils.translation import gettext as _

from utils import types
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    name :  types.CharField = models.CharField(max_length=128)
    email : types.CharField = models.CharField(max_length=64)
    phone = PhoneNumberField(null=True, blank=True)
    message : types.TextField = models.TextField(blank=True)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True, db_index=True)
    def __str__(self):
        return self.name