from django.db import models


class Regulation(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    sub_category = models.ForeignKey("SubCategory", on_delete=models.CASCADE)
    regime = models.ForeignKey("Regime", on_delete=models.CASCADE)

    text = models.ManyToManyField("TextSection")


class Category(models.Model):
    identifier = models.IntegerField()
    name = models.CharField(max_length=256)


class SubCategory(models.Model):
    identifier = models.CharField(max_length=256)
    name = models.CharField(max_length=256)


class Regime(models.Model):
    identifier = models.IntegerField()


class TextSection(models.Model):
    text = models.TextField()
    parent = models.ForeignKey("TextSection", null=True, on_delete=models.CASCADE)
    note = models.BooleanField()
