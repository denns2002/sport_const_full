from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from mailings.utils.change_email import change_email
from users.serializers.user_serializer import (ChangePasswordSerializer,
                                               ChangeEmailSerializer)


class ChangePasswordAPIView(GenericAPIView):
    """
    Changing password for auth users in update profile page.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    model = get_user_model()

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {"OK": "Password updated successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ChangeEmailAPIView(GenericAPIView):
#     """
#     Changing email for auth users in update profile page.
#     """
#
#     serializer_class = ChangeEmailSerializer
#
#     def post(self, request):
#         user = request.user
#         new_email = request.data.email
#
#         if user['email']:
#             change_email(user['email'], new_email, request)
#
#         return Response({"OK": "Check new email to confirm email change"},
#                         status=status.HTTP_200_OK)
#
#
# class ChangeEmailVerifyAPIView(GenericAPIView):
#     """
#     Verify new email address from email
#     """
#
#     pass
