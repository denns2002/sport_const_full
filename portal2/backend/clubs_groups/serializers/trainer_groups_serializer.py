from rest_framework import serializers

from clubs_groups.models.group import Group, GroupMember
from profiles.models.profile import Profile


class TrainerGroupsSerializer(serializers.ModelSerializer):
    groupmember_count = serializers.IntegerField(source='groupmember_set.count', read_only=True)

    # members_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = ('name', 'groupmember_count', 'slug')

    def get_members_count(self, language):
        return language.groupmembers.count()


class TrainerGroupMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='profile.first_name', read_only=True)
    last_name = serializers.CharField(source='profile.last_name', read_only=True)
    mid_name = serializers.CharField(source='profile.mid_name', read_only=True)
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)
    rank = serializers.CharField(source='profile.rank.name', read_only=True)
    slug = serializers.SlugField(source='profile.slug', read_only=True)
    id = serializers.IntegerField(source='profile.user.id')

    # @property
    # def debts_sum(self):
    #     sum_price = self.debts_set.objects.all().aggregate(price_sum=models.Sum('debts_set.price'))
    #     return sum_price['price_sum']

    class Meta:
        model = GroupMember
        fields = ['annual_fee', 'first_name', 'last_name', 'mid_name', 'avatar', 'rank', 'slug', 'id']


class TrainerGroupDetailSerializer(serializers.ModelSerializer):
    groupmember_set = TrainerGroupMemberSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ['groupmember_set', 'name']
