from django.contrib.auth.models import GroupManager
from rest_framework import serializers

from clubs_groups.models.group import Group, GroupMember
from profiles.models.profile import Profile
from profiles.serializers.profile_serializer import ProfileSerializer


class GroupMemberSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = GroupMember
        fields = ["profile", "group"]


class GroupSerializer(serializers.ModelSerializer):
    groupmembers = GroupMemberSerializer(many=True, source='groupmember_set')
    trainers = ProfileSerializer(many=True)

    class Meta:
        model = Group
        fields = ['name', 'slug', 'trainers', 'groupmembers']


# class DebtsSerializer(serializers.ModelSerializer):
#     remainder = serializers.IntegerField(source='get_remainder', read_only=True)
#
#     class Meta:
#         model = Debts
#         fields = ['name', 'price', 'paid', 'is_active', 'remainder']
#
#
# class GroupMemberDebtsSerializer(serializers.ModelSerializer):
#     debts_set = DebtsSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = GroupMember
#         fields = ['debts_set']


class GroupMemberChangeSerializer(serializers.ModelSerializer):
    group = serializers.SlugField(source='group.slug')

    class Meta:
        model = GroupMember
        fields = ["group"]

    def update(self, instance, validated_data):
        if 'group' in validated_data:
            instance.group = Group.objects.get(slug=validated_data['group']['slug'])

        instance.save()

        return instance


class TrainerChangeSerializer(serializers.ModelSerializer):
    trainers = serializers.CharField()

    class Meta:
        model = Group
        fields = ['trainers']

    def update(self, instance, validated_data):
        if 'trainers' in validated_data:
            trainer = Profile.objects.filter(slug=validated_data['trainers']).first()
            if trainer:
                if trainer in instance.trainers.all():
                    instance.trainers.remove(Profile.objects.get(slug=validated_data['trainers']).id)
                else:
                    instance.trainers.add(Profile.objects.get(slug=validated_data['trainers']).id)
                if Group.objects.filter(trainers__id=trainer.id):
                    trainer.is_trainer = True
                else:
                    trainer.is_trainer = False
                trainer.save()

            else:
                raise ValueError()

        instance.save()

        return instance
