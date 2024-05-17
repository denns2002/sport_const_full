from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     ListAPIView,
                                     UpdateAPIView,
                                     RetrieveAPIView)
from rest_framework.response import Response

from clubs_groups.models.group import Group, GroupMember
from clubs_groups.serializers.group_serializer import GroupSerializer, GroupMemberChangeSerializer, TrainerChangeSerializer
from clubs_groups.serializers.trainer_groups_serializer import TrainerGroupsSerializer, TrainerGroupDetailSerializer
from profiles.models.profile import Profile


class GroupListAPIView(ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class GroupDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = "slug"


class TrainerGroupListAPIView(ListAPIView):
    serializer_class = TrainerGroupsSerializer

    def get_queryset(self):
        trainer = Profile.objects.get(user=self.request.user.id)
        groups = Group.objects.filter(trainers__id=trainer.id)

        return groups


class TrainerGroupDetailAPIView(TrainerGroupListAPIView, RetrieveAPIView):
    serializer_class = TrainerGroupDetailSerializer
    lookup_field = "slug"


class GroupTrainerChangeAPIView(UpdateAPIView):
    serializer_class = TrainerChangeSerializer
    lookup_field = "slug"
    queryset = Group.objects.all()

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

    # def get_queryset(self):
    #     return Group.objects.filter(slug=self.kwargs["slug"])


# class GroupMemberDebtsAPIView(ListAPIView):
#     serializer_class = GroupMemberDebtsSerializer
#     lookup_field = "slug"
#
#     def get_queryset(self):
#         group_members = GroupMember.objects.filter(profile__slug=self.kwargs["slug"])
#         return group_members


class GroupMemberChangeAPIView(UpdateAPIView):
    serializer_class = GroupMemberChangeSerializer
    # queryset = GroupMember.objects.all()
    lookup_field = "profile__slug"

    def get_queryset(self):
        return GroupMember.objects.filter(profile__slug=self.kwargs["profile__slug"])
