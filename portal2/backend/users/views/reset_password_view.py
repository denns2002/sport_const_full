from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.serializers.reset_password_serializer import (
    RequestPasswordResetSerializer,
    SetNewPasswordSerializer
)
from mailings.utils.reset_password import send_reset_password


class RequestPasswordResetAPIView(GenericAPIView):
    """
    Send password reset link with tokens to email if the user has
    forgotten the login password.
    """

    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        email = request.data.get("email", "")

        if get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.get(email=email)
            send_reset_password(user, request)

            return Response(
                {"OK": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"ERROR": "This email isn't registered"},
            status=status.HTTP_404_NOT_FOUND
        )


class PasswordTokenCheckAPI(GenericAPIView):
    """
    Token and uid verification.
    """

    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise DjangoUnicodeDecodeError

            return Response({
                "OK": True, "message": "Valid", "uidb64": uidb64, "token": token
            })

        except DjangoUnicodeDecodeError:
            return Response(
                {"ERROR": "Token is not valid, please request a new one"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SetNewPasswordAPIView(GenericAPIView):
    """
    Patch new password from email (needs uidb64 and token).
    """

    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(
                {"OK": True, "message": "Password reset success"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
