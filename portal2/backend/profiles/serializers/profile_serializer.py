from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.utils import model_meta

from phones.models import Phone
from phones.serializers.phone_serializer import PhoneSerinalizer
from users.serializers.user_serializer import UserSerializer
from profiles.models.profile import Profile, Rank


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    rank = RankSerializer()
    phones = PhoneSerinalizer(many=True)
    group = serializers.SlugField(source="groupmember_set.first.group.slug",
                                  read_only=True)
    club = serializers.SlugField(
        source="groupmember_set.first.group.club_set.first.slug",
        read_only=True)

    class Meta:
        model = Profile
        fields = (
            "is_trainer",
            "is_manager",
            "first_name",
            "last_name",
            "mid_name",
            "avatar",
            "birth_date",
            "updated_at",
            "slug",
            "rank",
            "next_rank",
            "club",
            "group",
            "user",
            "phones",
            "photos"
        )
        read_only_fields = ('slug', 'next_rank')

    def validate_username(self, value):
        user = self.context["request"].profile.user
        if get_user_model.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})

        return value

    def update(self, instance, validated_data):
        if 'rank' in validated_data:
            data = validated_data.pop('rank')

            try:
                rank = Rank.objects.get(name=data['name'])
                print(rank)
                instance.rank = rank

            except Rank.DoesNotExist:
                raise ValueError("Rank does not exist")

        if 'user' in validated_data:
            nested_serializer = self.fields['user']
            nested_instance = instance.user
            nested_data = validated_data.pop('user')

            nested_serializer.update(nested_instance, nested_data)

        if 'phones' in validated_data:
            data = validated_data.pop('phones')
            m2m = []
            for item in data:
                try:
                    phone = Phone.objects.get(number=item['number'])
                except Phone.DoesNotExist:
                    phone = None

                if not phone:
                    phone = Phone.objects.create(number=item['number'])

                m2m.append(phone)

            instance.phones.clear()
            for item in m2m:
                instance.phones.add(item.id)

        info = model_meta.get_field_info(instance)
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        instance.save()

        return instance


class TrainerRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)

    def create(self, validated_data):
        string = get_random_string(length=10)
        user = get_user_model().objects.create(
            username=string,
            is_verified=True,
        )
        user.set_password(string)
        user.save()

        profile = Profile.objects.create(**validated_data)
        profile.user = user
        profile.save()

        return {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "mid_name": profile.mid_name,
            "birth_date": profile.birth_date,
            "username": string,
            "password": string,
        }

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "mid_name",
            "birth_date",
            "username",
            "password"
        )


class TrainerListRegisterSerializer(serializers.ListSerializer):
    child = TrainerRegisterSerializer()
