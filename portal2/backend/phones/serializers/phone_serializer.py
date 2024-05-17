from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from phones.models import Phone


class PhoneSerinalizer(serializers.ModelSerializer):
    number = PhoneNumberField()

    class Meta:
        model = Phone
        fields = ['number']
