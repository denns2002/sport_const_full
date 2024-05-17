from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin

from .models.profile import *


class ProfileFields:
    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "id",
                    "slug",
                    "user",
                    "is_trainer",
                    "is_manager",
                    "first_name",
                    "last_name",
                    "mid_name",
                    "birth_date",
                    # "address",
                    "avatar_full",
                    "avatar",
                    "updated_at",
                    'phones'
                ),
            },
        ),
        ("Achievements in sports", {"fields": ("rank", "next_rank"), "classes": ("wide",)}),
        ("Photos", {"fields": ("photos",), "classes": ("wide",)}),
    )

    list_display = ["user", "avatar_tag", "first_name", "last_name", "mid_name"]

    search_fields = [
        "first_name",
        "last_name",
        "mid_name",
        "user__username",
        "user__email",
    ]
    list_filter = [
        "birth_date",
    ]
    readonly_fields = ["updated_at", "avatar_full", "next_rank", "id"]
    filter_horizontal = ["phones", "photos"]


@admin.register(Profile)
class ProfileAdmin(ProfileFields, admin.ModelAdmin):
    pass


# for user model admin
class ProfileInline(ProfileFields, SuperInlineModelAdmin, admin.StackedInline):
    model = Profile
    extra = 1


admin.site.register(Rank)
