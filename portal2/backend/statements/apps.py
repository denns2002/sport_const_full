from django.apps import AppConfig

from admincustom.utils.check_language import translate_ru


class StatementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "statements"
    verbose_name = translate_ru("Statements", "Ведомости")
