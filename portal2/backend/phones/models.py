from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from admincustom.utils.check_language import translate_ru


class Phone(models.Model):
    number = PhoneNumberField(unique=True, verbose_name=translate_ru("Phone", "Телефон"))

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Phone", "Phones"],
            ["Телефон", "Телефоны"]
        )

    def __str__(self):
        return str(self.number)
