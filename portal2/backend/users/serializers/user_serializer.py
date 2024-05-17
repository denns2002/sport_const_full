from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
            "is_active",
            "is_verified",
            "created_at",
            "updated_at",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"ERROR": "Password fields didn't match."}, 403
            )

        password = attrs.get("password")
        user = self.context["request"].user
        user.set_password(password)
        user.save()

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"ERROR": "Old password is not correct."}, 403
            )
        return value


class ChangeEmailSerializer(serializers.Serializer):
    class Meta:
        model = get_user_model()
        fields = ["email"]
