from django.db import models


class Regulation(models.Model):
    category = models.ForeignKey("Category")
    sub_category = models.ForeignKey("SubCategory")
    regime = models.ForeignKey("Regime")

    text = models.ManyToManyField("TextSection")


class Category(models.Model):
    identifier = models.IntegerField()
    name = models.CharField()


class SubCategory(models.Model):
    identifier = models.CharField()
    name = models.CharField()


class Regime(models.Model):
    identifier = models.IntegerField()


class TextSection(models.Model):
    text = models.TextField()
    parent = models.ForeignKey("TextSection", null=True)
    note = models.BooleanField()
