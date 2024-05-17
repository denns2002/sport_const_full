from django.urls import path

from clubs_groups.views.club import (ClubDetailAPIView,
                                     ClubListAPIView, ClubMenagerChangeAPIView)
from clubs_groups.views.group import (GroupDetailAPIView,
                               GroupListAPIView,
                               TrainerGroupListAPIView,
                               TrainerGroupDetailAPIView,
                               GroupTrainerChangeAPIView,
                               GroupMemberChangeAPIView,)

urlpatterns = [
    path("clubs/", ClubListAPIView.as_view(), name="clubs"),
    path("clubs/<slug:slug>/", ClubDetailAPIView.as_view(), name="club-detail"),
    path("clubs/change-manager/<slug:slug>/", ClubMenagerChangeAPIView.as_view(), name="clubs-manager-change"),
    path("groups/change-trainer/<slug:slug>/", GroupTrainerChangeAPIView.as_view(), name="groups-trainer-change"),
    path("groups/member-change/<slug:profile__slug>/", GroupMemberChangeAPIView.as_view(), name="groups-member-change"),

    path("groups/", GroupListAPIView.as_view(), name="group"),
    path("groups/<slug:slug>/", GroupDetailAPIView.as_view(), name="group-detail"),

    path("trainer-groups/", TrainerGroupListAPIView.as_view(), name="trainer-groups"),
    path("trainer-groups/<slug:slug>/", TrainerGroupDetailAPIView.as_view(), name="trainer-groups-detail"),


    # path("trainer-groups/debts/<slug:slug>/", GroupMemberDebtsAPIView.as_view(), name="trainer-groups-debts"),
    # отдельное приложение
    # урл для каждого пользователя по отдельности
]
