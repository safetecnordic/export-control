from django.contrib import admin
from regulations.models import *


class RegulationAdmin(admin.ModelAdmin):
    model = Regulation
    list_display = (
        "__str__",
        "category",
        "sub_category",
        "regime",
        "regime_number",
    )
    list_filter = ("category", "sub_category", "regime")


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "identifier",
        "name",
        "part",
    )
    list_filter = ("identifier",)


class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    list_display = (
        "identifier",
        "name",
    )
    list_filter = ("identifier",)


class RegimeAdmin(admin.ModelAdmin):
    model = Regime
    list_display = (
        "name",
        "number_range_max",
        "number_range_min",
    )
    list_filter = ("name",)


class ParagraphAdmin(admin.ModelAdmin):
    model = Paragraph
    list_display = (
        "__str__",
        "text",
        "order",
        "note",
        "parent",
    )
    list_filter = ("regulation",)


admin.site.register(Regulation, RegulationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Regime, RegimeAdmin)
admin.site.register(Paragraph, ParagraphAdmin)
