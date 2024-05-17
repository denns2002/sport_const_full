from django.contrib import admin
from django.contrib.auth import get_user_model
from super_inlines.admin import SuperModelAdmin

from profiles.admin import ProfileInline


@admin.register(get_user_model())
class UserAdmin(SuperModelAdmin):
    list_display = ["username", "email", "created_at", "updated_at"]
    search_fields = [
        "username",
        "email",
        "profile__first_name",
        "profile__last_name",
        "profile__mid_name",
        "profile__phone__number",
    ]
    list_filter = ["created_at", "updated_at"]
    fields = [
        "id",
        "username",
        "email",
        "is_staff",
        "is_active",
        "is_verified",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["id", "created_at", "updated_at"]
    inlines = [ProfileInline]
