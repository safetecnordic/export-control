from distutils.command.upload import upload
import black
from django.contrib.flatpages.models import FlatPage
from django.db import models
from utils import types  # type: ignore
from ckeditor.fields import RichTextField

class ExtendedFlatPage(FlatPage):
    title_description: types.CharField = models.CharField(max_length=256, null=True, blank=True)
    page_content: types.RichTextField = RichTextField(null=True, blank=True)
    image: types.ImageField = models.ImageField(null=True, blank=True, upload_to="flatpages/images")
    sidebar_title: types.CharField = models.CharField(max_length=256, null=True, blank=True)
    sidebar_text: types.RichTextField = RichTextField(null=True, blank=True)

    title_no: types.CharField = models.CharField(max_length=256, null=True, blank=True)
    title_description_no: types.CharField = models.CharField(max_length=256, null=True, blank=True)
    page_content_no: types.RichTextField = RichTextField(null=True, blank=True)
    sidebar_title_no: types.CharField = models.CharField(max_length=256, null=True, blank=True)
    sidebar_text_no: types.RichTextField = RichTextField(null=True, blank=True)