from django.apps import AppConfig

from admincustom.utils.check_language import translate_ru


class MailingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailings"
    verbose_name = translate_ru("Mailings", "Рассылки")
