from django.apps import AppConfig

from admincustom.utils.check_language import translate_ru


class ClubsGroupsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clubs_groups"
    verbose_name = translate_ru("Groups & Clubs", "Группы и клубы")
