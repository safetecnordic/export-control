from django.db import models
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    phone = PhoneNumberField(null=True, blank = True)
    message = models.TextField(blank=True)
    date_created = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name