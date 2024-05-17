from django.contrib import admin

from .models.statement import Statement, StatementMember

admin.site.register(StatementMember)


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    pass
