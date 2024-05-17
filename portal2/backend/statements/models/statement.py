from django.db import models

from events.models.event import Event
from profiles.models.profile import Profile


class Statement(models.Model):
    TYPES = [
        ("Группа", "Группа"),
        ("Свободный", "Свободный"),
        ("Мероприятие", "Мероприятие"),
    ]

    fio = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=255, choices=TYPES)


class StatementMember(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    attestation = models.BooleanField(default=False)
    seminar = models.BooleanField(default=False)
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, blank=True, null=True)
