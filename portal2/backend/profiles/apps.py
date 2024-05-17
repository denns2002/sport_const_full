from django.apps import AppConfig

from admincustom.utils.check_language import translate_ru


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "profiles"
    verbose_name = translate_ru("Profiles", "Профили")
