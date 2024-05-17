from django.apps import AppConfig

from admincustom.utils.check_language import translate_ru


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = translate_ru("Users", "Пользователи")
