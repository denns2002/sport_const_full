from datetime import date

import django_filters

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView, ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import AllowAny
from rest_framework import filters

from clubs_groups.models.group import Group
from events.models.event import Event, PlannedEvents
from events.serializers.event_serializer import (EventOrganizersSerializer,
                                                 EventSerializer,
                                                 PlannedEventSerializer,
                                                 EventCoOrganizersSerializer)
from statements.models.statement import Statement
from statements.serializers.statement import DownloadStatementSerializer


# class RegEndGTEFilterBacked(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(reg_end__gte=datetime.datetime.today())
#
#
# class RegEndLTEFilterBacked(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(reg_end__lte=datetime.datetime.today())

class EventFilter(django_filters.FilterSet):
    reg_end_gte = django_filters.DateFilter(field_name="reg_end", lookup_expr='gte')
    reg_end_lte = django_filters.DateFilter(field_name="reg_end", lookup_expr='lte')
    date_end_gte = django_filters.DateFilter(field_name="date_end", lookup_expr='gte')
    date_end_lte = django_filters.DateFilter(field_name="date_end", lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['is_attestation', 'is_seminar', 'reg_end_gte', 'reg_end_lte', 'date_end_gte']


class EventMixin(GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "slug"


class EventListCreateAPIView(ListCreateAPIView, EventMixin):
    """
    GET a list of all events.
    """

    permission_classes = [AllowAny]
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'address']
    filterset_fields = ["is_attestation", "is_seminar", "reg_end", "date_end"]
    ordering_fields = ['reg_end']
    ordering = ['reg_end']


class EventDetailAPIView(RetrieveUpdateDestroyAPIView, EventMixin):
    """
    GET event details.
    CRUD events for supervisors and organizers.
    """

    permission_classes = [AllowAny]


class EventAddOrgAPIView(UpdateAPIView):
    """
    Add organizers to events.

    - Gives full access to the event's CRUD.
    - The specified profiles will be in the contacts of the event.
    """

    queryset = Event.objects.all()
    serializer_class = EventOrganizersSerializer
    lookup_field = "slug"


class EventAddCoOrgAPIView(UpdateAPIView):
    """
    Add co-organizers to events.

    - The specified profiles will be in the contacts of the event.
    """

    queryset = Event.objects.all()
    serializer_class = EventCoOrganizersSerializer
    lookup_field = "slug"


class PlannedEventsAPIView(ListAPIView):
    """
    The trainer can view all upcoming events for which statements have been created.
    """

    serializer_class = PlannedEventSerializer

    def get_queryset(self):
        trainer = get_user_model().objects.get(id=self.request.user.id)
        groups = Group.objects.filter(trainers__id=trainer.id)
        planned_events = PlannedEvents.objects.filter(group__in=groups, event__date_end__gte=date.today())

        return planned_events


class EventStatementAPIView(RetrieveAPIView):

    def get_object(self):
        return Statement.objects.filter(event=self.kwargs['event_id']).last()

    serializer_class = DownloadStatementSerializer
    lookup_field = "event_id"

