from django.contrib import admin

from .models.event import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "id",
                    "slug",
                    "name",
                    "is_attestation",
                    "attestation_date",
                    "is_seminar",
                    "seminar_date",
                    "about",
                    "reg_start",
                    "reg_end",
                    "date_start",
                    "date_end",
                ),
            },
        ),
        (
            "Organizers",
            {
                "fields": ("organizers", "co_organizers"),
                "classes": ("wide",),
            },
        ),
        (
            "Members",
            {
                "fields": ("members",),
                "classes": ("wide",),
            },
        )
    )

    list_display = ["name", "is_attestation", "is_seminar", "date_start"]
    readonly_fields = ["id"]
    search_fields = ["name", "addresses", "about"]
    list_filter = ["date_start"]
    filter_horizontal = ["organizers", "co_organizers", "members"]
