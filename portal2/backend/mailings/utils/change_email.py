from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from mailings.utils.send_mail import send_email


# def change_email(old_email, new_email, request):
#     domain = get_current_site(request).domain
#     user = get_user_model().objects.get(email=old_email)
#
#     token = RefreshToken.for_user(user).access_token.
#     relative_link = reverse("change-email-verify")
#     url = f"http://{domain}{relative_link}?token={str(token)}"
#     email_body = "Hi, " + user.username + "!\nTo confirm your email " \
#                  "has been changed follow the link. \n" + url
#
#     send_email(
#         "Change email to Aikido Portal",
#         email_body,
#         [new_email]
#     )


    #
