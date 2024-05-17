import logging

import jwt
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.response import Response

from users.serializers.email_verify_serializer import EmailVerifySerializer
from config.settings import base as settings
from config.settings import packeges


class EmailVerifyAPIView(views.APIView):
    """
    Validates the token that came in the mail after registration.
    """

    serializer_class = EmailVerifySerializer

    @swagger_auto_schema(manual_parameters=[openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Access token",
        type=openapi.TYPE_STRING,
    )])
    def get(self, request):
        token = request.GET.get("token")

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=packeges.SIMPLE_JWT["ALGORITHM"]
            )
            user = get_user_model().objects.get(id=payload["user_id"])

            if not user.is_verified:
                user.is_verified = True
                user.save()

                return Response({"OK": "Successfully activated"},
                                status=status.HTTP_200_OK)

            return Response({"OK": "The account is already verified"})

        except jwt.ExpiredSignatureError as _:
            return Response({"ERROR": "Activation expired"},
                            status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as _:
            return Response({"ERROR": "Invalid token"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            logger = logging.getLogger(__name__)
            logger.error(error)
