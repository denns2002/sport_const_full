from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView, UpdateAPIView)
from rest_framework.response import Response

from clubs_groups.models.club import Club
from clubs_groups.serializers.club_serializer import ClubSerializer, \
    ClubMenagerSerializer
from profiles.models.profile import Profile


class ClubListAPIView(ListCreateAPIView):
    #фильтр по руководителям
    serializer_class = ClubSerializer
    queryset = Club.objects.filter()

    def get_queryset(self):
        return self.queryset.all()


class ClubDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    lookup_field = "slug"


class ClubMenagerChangeAPIView(UpdateAPIView):
    serializer_class = ClubMenagerSerializer
    lookup_field = "slug"
    queryset = Club.objects.all()

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except ValueError as e:
            return Response({"ERROR": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        try:
            return self.partial_update(request, *args, **kwargs)
        except ValueError as e:
            return Response({"ERROR": "User not found"}, status=status.HTTP_404_NOT_FOUND)
