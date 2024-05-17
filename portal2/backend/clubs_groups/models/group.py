from django.db import models
from django.utils.crypto import get_random_string

from profiles.models.profile import Profile
from admincustom.utils.check_language import translate_ru


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name=translate_ru("Name", "Название"))
    slug = models.SlugField(max_length=55, blank=True, verbose_name=translate_ru("URL", "Ссылка"))
    trainers = models.ManyToManyField(
        Profile,
        blank=True,
        verbose_name=translate_ru("Trainers", "Тренера"),
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = get_random_string(length=10)

            while Group.objects.filter(slug=slug).exists():
                slug = slug + get_random_string(length=10)

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return " - " + str(self.name)

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Group", "Groups"],
            ["Группа", "Группы"]
        )


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=translate_ru("Group", "Группа"), blank=True, null=True)
    profile = models.ForeignKey(
        Profile,
        unique=True,
        on_delete=models.CASCADE,
        verbose_name=translate_ru("Profile", "Профиль"),
    )
    annual_fee = models.BooleanField(default=False, verbose_name=translate_ru("Annual Fee", "Ежегодная выплата"))

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Group Member", "Group Members"],
            ["Участник группы", "Участники группы"]
        )




# class Debts(models.Model):
#     member = models.ForeignKey(
#         GroupMember,
#         on_delete=models.CASCADE,
#         verbose_name=check_language("Member", "Участник"),
#     )
#     is_active = models.BooleanField(default=True, verbose_name=check_language("Is active", "Активна"))
#     name = models.CharField(max_length=255, verbose_name=check_language("Name", "Название"))
#     price = models.IntegerField(default=0, verbose_name=check_language("Price", "Стоимость"))
#     paid = models.IntegerField(default=0, verbose_name=check_language("Paid", "Выплачено"))
#
#     def get_remainder(self):
#         return int(self.price) - int(self.paid)
#
#     class Meta:
#         if check_ru_lang():
#             verbose_name = "Задолжность"
#             verbose_name_plural = "Задолжности"
#         else:
#             verbose_name = "Debt"
#             verbose_name_plural = "Debts"
