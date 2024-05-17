from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin

from photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    fields = ["name", "link", "uploaded_at", "photo_full"]
    readonly_fields = ["photo_full", "uploaded_at"]
    list_display = ["name", "photo_tag"]
