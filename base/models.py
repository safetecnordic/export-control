from django.contrib.flatpages.models import FlatPage
from django.db import models
from utils import types  # type: ignore
from ckeditor.fields import RichTextField


class ExtendedFlatPage(FlatPage):
    title_no: types.CharField = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="title (Norwegian)"
    )

    description: types.CharField = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="description (English)"
    )
    description_no: types.CharField = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="description (Norwegian)"
    )

    page_content: types.RichTextField = RichTextField(null=True, blank=True, verbose_name="page content (English)")
    page_content_no: types.RichTextField = RichTextField(null=True, blank=True, verbose_name="page content (Norwegian)")

    sidebar_title: types.CharField = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="sidebar title (English)"
    )
    sidebar_title_no: types.CharField = models.CharField(
        max_length=256, null=True, blank=True, verbose_name="sidebar title (Norwegian)"
    )

    sidebar_text: types.RichTextField = RichTextField(null=True, blank=True, verbose_name="sidebar text (English)")
    sidebar_text_no: types.RichTextField = RichTextField(null=True, blank=True, verbose_name="sidebar text (Norwegian)")

    image: types.ImageField = models.ImageField(
        null=True, blank=True, upload_to="flatpages/images", verbose_name="sidebar image"
    )

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"
