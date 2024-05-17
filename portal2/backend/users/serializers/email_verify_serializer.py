from django.contrib.auth import get_user_model
from rest_framework import serializers


class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = get_user_model()
        fields = ["token"]
