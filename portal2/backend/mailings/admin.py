from django.contrib import admin

from mailings.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    fields = ['subject', 'is_error', 'time', 'from_email', 'body', 'recipients']
    list_display = ['subject', 'is_error', 'from_email', 'time']
    list_filter = ['is_error']
    search_fields = [
        'subject',
        'from_email',
        'body',
        # 'recipients__profile__',
        'time']
    readonly_fields = fields
    filter_horizontal = ['recipients']
