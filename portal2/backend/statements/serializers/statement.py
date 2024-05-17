from rest_framework import serializers

from clubs_groups.models.club import Club
from clubs_groups.models.group import GroupMember
from events.models.event import Event
from statements.models.statement import Statement, StatementMember
from profiles.models.profile import Profile, Rank

import spreadsheets_api.spreads as s


class StatementMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementMember
        fields = [
            "member",
            "attestation",
            "seminar",
        ]


class GroupStatementSerializer(serializers.ModelSerializer):
    """
    {
      "statementmember_set": [
        {
          "member": 0,
          "attestation": true,
          "seminar": true
        },

        {
          "member": 1,
          "attestation": true,
          "seminar": true
        },
      ],
      "event": 0
    }
    """

    statementmember_set = StatementMemberSerializer(many=True)

    class Meta:
        model = Statement
        fields = ["id", "created_at", "link", "statementmember_set", "event"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        members = []
        event = validated_data['event']
        st_members = []
        for item in validated_data["statementmember_set"]:

            profile = Profile.objects.get(id=item["member"].id)
            event.members.add(profile.user)
            event.save()
            fio = f"{str(profile.first_name)} {str(profile.last_name)}"
            st_members.append(StatementMember.objects.create(
                member=profile,
                attestation=item["attestation"],
                seminar=item["seminar"]
            ))

            if profile.mid_name:
                fio += f" {str(profile.mid_name)}"
            try:
                groupmember = GroupMember.objects.get(profile=item["member"].id)
                group = groupmember.group
                trainer = group.trainers.first()
                trainer_fio = f"{str(trainer.first_name)} {str(trainer.last_name)}"

                if trainer.mid_name:
                    trainer_fio += f" {str(trainer.mid_name)}"

                club = Club.objects.get(groups=group.id)
                club_name = club.name
                annual = groupmember.annual_fee

            except:
                trainer_fio = ''
                annual = False
                club_name = ''

            try:
                city = event.address
            except:
                city = ''

            member = {
                "fio": fio,
                "rank": Rank.objects.get(id=profile.rank.id).name if profile.rank else 'Нет',
                "next_rank": Rank.objects.get(id=profile.next_rank.id).name if profile.rank else 'Нет',
                "annual_fee": annual,
                "group_type": 'детская',
                "trainer_fio": trainer_fio,
                "club": club_name,
                "city": city,
                "attestation_date": None,
                "seminar_date": None,
            }

            if event.is_attestation:
                attestation_date = '%s/%s/%s' % (
                    event.attestation_date.day,
                    event.attestation_date.month,
                    event.attestation_date.year)
                member['attestation_date'] = attestation_date

            if event.is_seminar:
                seminar_date = '%s/%s/%s' % (
                    event.seminar_date.day,
                    event.seminar_date.month,
                    event.seminar_date.year)
                member['seminar_date'] = seminar_date

            members.append(member)

        services = s.start_services('credentials.json')
        batch_update_structure_body = {"requests": []}
        batch_update_values_data = []
        values = []

        for i in range(len(members)):
            inside_values = [i + 1,
                             members[i]['fio'],
                             members[i]['rank'],
                             members[i]['trainer_fio'],
                             members[i]['group_type'],
                             'Обычная',
                             members[i]['next_rank'],
                             members[i]['annual_fee'],
                             members[i]['seminar_date'],
                             members[i]['attestation_date'],
                             'Нет',
                             'Нет'
                             ]
            values.append(inside_values)

        s.prepare_spreadsheet_values_data(f'A7:L{6 + len(members)}',
                                          "ROWS",
                                          batch_update_values_data,
                                          values)
        s.prepare_filter_set_basic_request(batch_update_structure_body)
        spreadsheet_id = s.create_sample(
            "Ведомость",
            services['service'],
            services['drive_service'],
            10 + len(members),
            batch_update_values_data,
            batch_update_structure_body,
            members[0]["city"],
            members[0]["club"]
        )
        link = "https://docs.google.com/spreadsheets/d/" + spreadsheet_id + "/edit#gid=0"

        statement = Statement(
            link=link,
            event=validated_data['event'],
            type='group'
        )
        statement.save()

        for m in st_members:
            m.statement = statement
            m.save()

        return statement


class FreeStatementSerializer(serializers.ModelSerializer):
    """
    {
      "fio": "string",
      "is_child": false
    }
    """

    fio = serializers.CharField(max_length=255)

    class Meta:
        model = Statement
        fields = ["fio", "event"]

    def create(self, validated_data):
        link = ''
        statement = Statement(
            link=link,
            event=validated_data['event'],
            type='Свободный'
        )
        statement.save()

        fio = validated_data['fio'].split()
        profile = Profile.objects.create(
            first_name=fio[0],
            last_name=fio[1],
            mid_name=fio[2]
        )

        StatementMember.objects.create(
            member=profile,
            statement=statement
        )
        return statement


class EventStatementSerializer(serializers.ModelSerializer):
    """
    {
      "event": 0
    }
    """

    event = serializers.SlugField()

    class Meta:
        model = Statement
        fields = ["id", "created_at", "link", "event"]
        read_only_fields = ["id", "created_at", "link"]

    def create(self, validated_data):
        statements = Statement.objects.filter(event__slug=validated_data['event'])
        event = Event.objects.get(slug=validated_data['event'])
        members_all = []

        for st in statements:
            for m in StatementMember.objects.filter(statement=st):
                members_all.append(m)

        members = []

        for item in members_all:

            profile = Profile.objects.get(id=item.member.id)
            event.members.add(profile.user)
            event.save()
            fio = f"{str(profile.first_name)} {str(profile.last_name)}"
            print(fio)

            if profile.mid_name:
                fio += f" {str(profile.mid_name)}"

            try:
                groupmember = GroupMember.objects.get(profile=item.member.id)
                group = groupmember.group
                trainer = group.trainers.first()
                trainer_fio = f"{str(trainer.first_name)} {str(trainer.last_name)}"

                if trainer.mid_name:
                    trainer_fio += f" {str(trainer.mid_name)}"

                club = Club.objects.get(groups=group.id)
                club_name = club.name
                annual = groupmember.annual_fee

            except:
                trainer_fio = ''
                annual = False
                club_name = ''

            try:
                city = event.address
            except:
                city = ''

            member = {
                "fio": fio,
                "rank": Rank.objects.get(
                    id=profile.rank.id).name if profile.rank else 'Нет',
                "next_rank": Rank.objects.get(
                    id=profile.next_rank.id).name if profile.rank else 'Нет',
                "annual_fee": annual,
                "group_type": 'детская',
                "trainer_fio": trainer_fio,
                "club": club_name,
                "city": city,
                "attestation_date": None,
                "seminar_date": None,
            }

            if event.is_attestation:
                attestation_date = '%s/%s/%s' % (
                    event.attestation_date.day,
                    event.attestation_date.month,
                    event.attestation_date.year)
                member['attestation_date'] = attestation_date

            if event.is_seminar:
                seminar_date = '%s/%s/%s' % (
                    event.seminar_date.day,
                    event.seminar_date.month,
                    event.seminar_date.year)
                member['seminar_date'] = seminar_date

            members.append(member)

        services = s.start_services('credentials.json')
        batch_update_structure_body = {"requests": []}
        batch_update_values_data = []
        values = []

        for i in range(len(members)):
            inside_values = [i + 1,
                             members[i]['fio'],
                             members[i]['rank'],
                             members[i]['trainer_fio'],
                             members[i]['group_type'],
                             'Обычная',
                             members[i]['next_rank'],
                             members[i]['annual_fee'],
                             members[i]['seminar_date'],
                             members[i]['attestation_date'],
                             'Нет',
                             'Нет'
                             ]
            values.append(inside_values)

        s.prepare_spreadsheet_values_data(f'A7:L{6 + len(members)}',
                                          "ROWS",
                                          batch_update_values_data,
                                          values)
        s.prepare_filter_set_basic_request(batch_update_structure_body)
        spreadsheet_id = s.create_sample(
            "Ведомость",
            services['service'],
            services['drive_service'],
            10 + len(members),
            batch_update_values_data,
            batch_update_structure_body,
            members[0]["city"],
            members[0]["club"]
        )
        link = "https://docs.google.com/spreadsheets/d/" + spreadsheet_id + "/edit#gid=0"

        statement = Statement(
            link=link,
            event=event,
            type='group'
        )
        statement.save()

        return statement


class DownloadStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = '__all__'
