from rest_framework import serializers

from events.models.event import Event, PlannedEvents
from statements.models.statement import Statement


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventOrganizersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["organizers"]


class EventCoOrganizersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["co_organizers"]


class PlannedEventSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = PlannedEvents
        fields = ["event"]

