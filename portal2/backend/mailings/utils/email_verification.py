from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from mailings.models import Mailing
from mailings.utils.send_mail import send_email


def send_verify_email(user_data, request):
    """
    Sends a confirmation link by email. (refresh token)
    """

    try:
        user = get_user_model().objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token
        domain = get_current_site(request).domain
        relative_link = reverse("email-verify")
        url = f"http://{domain}{relative_link}?token={str(token)}"
        email_body = "Hi, " + user.username + \
                     "!\nUse link to verify your email. \n" + url

        data = [
            "Verify your email",
            email_body,
            [user.email]
        ]

    except Exception as error:
        Mailing.objects.create(
            is_error=True,
            error=error,
            subject="Verify your email",
        )

    else:
        send_email(*data)
