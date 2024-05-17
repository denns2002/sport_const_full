from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin

from clubs_groups.models.club import Club
from clubs_groups.models.group import Group, GroupMember


class GroupMemberInline(SuperInlineModelAdmin, admin.StackedInline):
    model = GroupMember
    extra = 1


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ["name"]
    filter_horizontal = ["groups", "photos", "managers"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    filter_horizontal = ["trainers"]
    inlines = [GroupMemberInline]

