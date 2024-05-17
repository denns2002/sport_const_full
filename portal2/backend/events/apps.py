from django.apps import AppConfig

from admincustom.utils.check_language import translate_ru


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"
    verbose_name = translate_ru("Events", "Мероприятия")
