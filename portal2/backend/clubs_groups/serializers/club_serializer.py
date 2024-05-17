from rest_framework import serializers

from clubs_groups.models.club import Club
from profiles.models.profile import Profile
from profiles.serializers.profile_serializer import ProfileSerializer


class ClubSerializer(serializers.ModelSerializer):
    managers = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = [
            "name",
            "info",
            "address",
            "slug",
            "groups",
            "managers",
            "photos",
            "is_active",
        ]


class ClubMenagerSerializer(serializers.ModelSerializer):
    managers = serializers.CharField()

    class Meta:
        model = Club
        fields = ['managers']

    def update(self, instance, validated_data):
        if 'managers' in validated_data:
            manager = Profile.objects.filter(slug=validated_data['managers']).first()
            if manager:
                if manager in instance.managers.all():
                    instance.managers.remove(Profile.objects.get(slug=validated_data['managers']).id)
                    print('re')
                else:
                    instance.managers.add(Profile.objects.get(slug=validated_data['managers']).id)
                if Club.objects.filter(managers__id=manager.id):
                    manager.is_manager = True
                else:
                    manager.is_manager = False
                manager.save()

            else:
                raise ValueError()

        instance.save()

        return instance
