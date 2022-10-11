from email.mime import message
from xmlrpc.client import DateTime
from django.db import models
from django.forms import CharField
from datetime import datetime

class Contact(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    message = models.TextField(blank=True)
    date_created = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name