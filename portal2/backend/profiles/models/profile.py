from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from transliterate import translit
from django.db import models

from admincustom.utils.check_language import translate_ru
from phones.models import Phone
from photos.models import Photo


class Rank(models.Model):
    RANKS = (
        [(str(x) + " кю детский", str(x) + " кю детский") for x in range(6, 0, -1)]
        + [(str(x) + " кю", str(x) + " кю") for x in range(5, 0, -1)]
        + [(str(x) + " дан", str(x) + " дан") for x in range(1, 6)]
        + [("Нет", "Нет")]
    )
    name = models.CharField(
        max_length=255,
        choices=RANKS,
        verbose_name=translate_ru("Name", "Название")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Rank", "Ranks"],
            ["Ранг", "Ранги"]
        )


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        verbose_name=translate_ru("User", "Пользователь"),
    )
    is_trainer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    first_name = models.CharField(
        max_length=255,
        verbose_name=translate_ru("First Name", "Имя")
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=translate_ru("Last Name", "Фамилия")
    )
    mid_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=translate_ru("Mid Name", "Отчество")
    )
    avatar = models.ImageField(
        upload_to="photo/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name=translate_ru("Avatar", "Аватар"),
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=translate_ru("Birth Date", "День рождения"),
    )
    # address = models.ForeignKey(
    #     Address,
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     verbose_name=translate_ru("City", "Город"),
    # )
    rank = models.ForeignKey(
        Rank,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=translate_ru("Rank", "Ранг"),
        related_name="rank",
    )
    next_rank = models.ForeignKey(
        Rank,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=translate_ru("Next Rank", "Следующий Ранг"),
        related_name="next_rank",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=translate_ru("Updated at", "Обновлен")
    )
    slug = models.SlugField(
        max_length=55,
        blank=True,
        verbose_name=translate_ru("URL", "Ссылка")
    )
    phones = models.ManyToManyField(
        Phone,
        verbose_name=translate_ru("Phones", "Телефоны"),
        blank=True
    )
    photos = models.ManyToManyField(
        Photo,
        verbose_name=translate_ru("Photos", "Фото"),
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = str(self.first_name) + str(self.last_name) + str(self.mid_name)
            slug = translit(slug[:10], language_code="ru", reversed=True)
            slug = slugify(slug) + get_random_string(length=10)

            while Profile.objects.filter(slug=slug).exists():
                slug = slug + get_random_string(length=4)

            self.slug = slug

        self.first_name = str(self.first_name)[0].upper() + str(self.first_name)[1:]
        self.last_name = str(self.last_name)[0].upper() + str(self.last_name)[1:]
        self.mid_name = str(self.mid_name)[0].upper() + str(self.mid_name)[1:] if self.mid_name else None
        self.next_rank = Rank.objects.get(id=self.rank.id + 1) if self.rank else None

        super().save(*args, **kwargs)

    def __str__(self):
        string = [item for item in [self.first_name, self.mid_name, self.last_name] if item]
        return " ".join(string)

    def get_avatar(self):
        if not self.avatar:
            return "/static/images/user.jpg"

        return self.avatar.url

    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())

    def avatar_full(self):
        return mark_safe('<img src="%s" width="200" />' % self.get_avatar())

    avatar_tag.short_description = \
        avatar_full.short_description = translate_ru("Avatar", "Аватарка")

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Profile", "Profiles"],
            ["Профиль", "Профили"]
        )
