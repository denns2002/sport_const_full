from django.db import models
from django.utils.crypto import get_random_string
from transliterate import slugify, translit

from clubs_groups.models.group import Group
from photos.models import Photo
from admincustom.utils.check_language import translate_ru
from profiles.models.profile import Profile


class Club(models.Model):
    name = models.CharField(max_length=255, verbose_name=translate_ru("Name", "Название"))
    info = models.TextField(verbose_name=translate_ru("Info", "Информация"))
    address = models.CharField(max_length=255, verbose_name=translate_ru("Address", "Адрес"), null=True, blank=True)
    slug = models.SlugField(max_length=55, blank=True, verbose_name=translate_ru("URL", "Ссылка"))
    groups = models.ManyToManyField(Group, blank=True, verbose_name=translate_ru("Groups", "Группы"))
    photos = models.ManyToManyField(Photo, blank=True, verbose_name=translate_ru("Photos", "Фото"))
    is_active = models.BooleanField(default=True, verbose_name=translate_ru("Active", "Активно"))
    managers = models.ManyToManyField(
        Profile,
        blank=True,
        verbose_name=translate_ru("Managers", "Руководители"),
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = translit(str(self.name)[:10], language_code="ru", reversed=True)
            slug = slugify(slug, language_code="uk") + get_random_string(length=10)

            while Club.objects.filter(slug=slug).exists():
                slug = slug + get_random_string(length=4)

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Club", "Clubs"],
            ["Клуб", "Клубы"]
        )
