from django.contrib import admin
from regulations.models import *


class RegulationAdmin(admin.ModelAdmin):
    model = Regulation
    list_display = (
        "category",
        "sub_category",
        "regime",
        "regime_number",
    )


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "identifier",
        "name",
        "part",
    )


class SubCategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "identifier",
        "name",
    )


class RegimeAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "name",
        "number_range_max",
        "number_range_min",
    )


class ParagraphAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "text",
        "order",
        "note",
        "parent",
    )


admin.site.register(Regulation, RegulationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Regime, RegimeAdmin)
admin.site.register(Paragraph, ParagraphAdmin)
