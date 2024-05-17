from django.db import models
from django.utils.safestring import mark_safe

from admincustom.utils.check_language import translate_ru


class Photo(models.Model):
    name = models.CharField(max_length=255, verbose_name=translate_ru("Name", "Название"))
    link = models.ImageField(upload_to="photo/%Y/%m/%d/", verbose_name=translate_ru("Link", "Ссылка"), unique=True)
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name=translate_ru("Uploaded at", "Загружено")
    )

    def get_photo(self):
        if not self.link:
            return "/static/images/user.jpg"
        return self.link.url

    def photo_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_photo())

    def photo_full(self):
        return mark_safe('<img src="%s" width="200" />' % self.get_photo())

    photo_tag.short_description = photo_full.short_description = "Фото" if translate_ru() else "Photo"

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Photo", "Photos"],
            ["Фото", "Фото"]
        )

    def __str__(self):
        return str(self.name)
