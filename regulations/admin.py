from django.contrib import admin
from regulations.models import *
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class RegulationAdmin(admin.ModelAdmin):
    model = Regulation
    list_display = (
        "code",
        "category",
        "sub_category",
        "regime",
    )
    ordering = ("code",)
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


class ParagraphAdmin(TreeAdmin):
    class Media:
        css = {"all": ("base/css/admin.css",)}

    form = movenodeform_factory(Paragraph)
    list_display = (
        "code",
        "text",
    )
    list_filter = ("category", "sub_category", "regulation")


admin.site.register(Regulation, RegulationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Regime, RegimeAdmin)
admin.site.register(Paragraph, ParagraphAdmin)
