from distutils.command.upload import upload
from django.contrib.flatpages.models import FlatPage
from django.db import models

class ExtendedFlatPage(FlatPage):
    image = models.ImageField(null=True, blank=True, upload_to="flatpages/images")
