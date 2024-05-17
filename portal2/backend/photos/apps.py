from django.apps import AppConfig

from admincustom.utils.check_language import translate_ru


class PhotosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "photos"
    verbose_name = translate_ru("Photos", "Фото")
