from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string

from clubs_groups.models.group import Group
from admincustom.utils.check_language import translate_ru


class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name=translate_ru("Name", "Название"))
    reg_start = models.DateField(verbose_name=translate_ru("Start of registration", "Начало регистрации"))
    reg_end = models.DateField(verbose_name=translate_ru("End of registration", "Окончание регистрации"))
    date_start = models.DateField(verbose_name=translate_ru("Start date", "Дата начала"))
    date_end = models.DateField(verbose_name=translate_ru("End date", "Дата окончания"))
    address = models.CharField(max_length=255, verbose_name=translate_ru("Address", "Адрес"), null=True, blank=True)
    about = models.TextField(verbose_name=translate_ru("About", "Описание"))
    organizers = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="organizers",
        verbose_name=translate_ru("Organizers", "Организаторы"),
    )
    co_organizers = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="co_organizers",
        verbose_name=translate_ru("Co-organizers", "Соорганизаторы"),
    )
    is_attestation = models.BooleanField(
        default=False, verbose_name=translate_ru("Is attestation", "Аттестация")
    )
    attestation_date = models.DateTimeField(
        blank=True, null=True, verbose_name=translate_ru("Attestation date", "Дата и время аттестации")
    )
    is_seminar = models.BooleanField(default=False, verbose_name=translate_ru("Is seminar", "Семинар"))
    seminar_date = models.DateTimeField(
        blank=True, null=True, verbose_name=translate_ru("Seminar date", "Дата и время семинара")
    )
    slug = models.SlugField(max_length=55, blank=True, verbose_name=translate_ru("URL", "Ссылка"))
    members = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="members",
        verbose_name=translate_ru("Members", "Участники"),
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            slug = get_random_string(length=10)

            while Event.objects.filter(slug=slug).exists():
                slug = get_random_string(length=10)

            self.slug = slug

        super(Event, self).save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Event", "Events"],
            ["Мероприятие", "Мероприятия"]
        )


class PlannedEvents(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

