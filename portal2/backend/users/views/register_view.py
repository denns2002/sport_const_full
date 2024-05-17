from rest_framework import generics, status
from rest_framework.response import Response

from users.serializers.register_serializer import RegisterSerializer
from mailings.utils.email_verification import send_verify_email


class RegisterAPIView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Register and send email verify if the user is not verified.
        """

        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        if user['email'] and not user['is_verified']:
            send_verify_email(user_data, request)

        return Response(user_data, status=status.HTTP_201_CREATED)
