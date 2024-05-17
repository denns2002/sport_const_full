from django.apps import AppConfig

from admincustom.utils.check_language import translate_ru


class PhonesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "phones"
    verbose_name = translate_ru("Phones", "Номера телефонов")
