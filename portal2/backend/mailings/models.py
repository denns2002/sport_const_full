from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from admincustom.utils.check_language import translate_ru


class Mailing(models.Model):
    is_error = models.BooleanField(
        default=False,
        verbose_name=translate_ru("Error", "Была ошибка")
    )
    error = models.TextField(
        verbose_name=translate_ru("Error", "Ошибка"),
        blank=True,
        null=True
    )
    subject = models.CharField(
        max_length=255,
        verbose_name=translate_ru("Subject", "Тема письма"),
        blank=True,
        null=True
    )
    body = models.TextField(
        verbose_name=translate_ru("Body", "Текст"),
        blank=True,
        null=True
    )
    recipients = models.ManyToManyField(get_user_model())
    from_email = models.CharField(
        max_length=255,
        default=settings.EMAIL_HOST_USER + settings.EMAIL_DOMAIN,
        verbose_name=translate_ru("From", "От"),
        blank=True,
        null=True
    )
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name, verbose_name_plural = translate_ru(
            ["Mailing", "Mailings"],
            ["Рассылка", "Рассылки"]
        )
