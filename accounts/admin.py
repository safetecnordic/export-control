from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


class UserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
    )
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"


admin.site.register(User, UserAdmin)
