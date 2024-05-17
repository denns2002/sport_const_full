from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from users.views.email_verify_view import EmailVerifyAPIView
from users.views.login_view import LoginAPIView
from users.views.logout_view import LogoutAPIView
from users.views.register_view import RegisterAPIView
from users.views.reset_password_view import (PasswordTokenCheckAPI,
                                             RequestPasswordResetAPIView,
                                             SetNewPasswordAPIView)
from users.views.user_view import ChangePasswordAPIView

urlpatterns = [
    # Default Auth URLs
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    # path("register/", RegisterAPIView.as_view(), name="register"),
    path("email-verify/",  # Registration verification from email
         EmailVerifyAPIView.as_view(),
         name="email-verify"),

    # Reset password
    path("request-pass-reset/",  # Request to reset password by email
         RequestPasswordResetAPIView.as_view(),
         name="request-pass-reset",),
    path("password-reset/<uidb64>/<token>/",  # Check uidb64 and token
         PasswordTokenCheckAPI.as_view(),
         name="password-reset-confirm",),
    path("password-reset-complete/",  # Complete password reset
         SetNewPasswordAPIView.as_view(),
         name="password-reset-complete",),

    # path("change-email/",  # Change email
    #      ChangeEmailAPIView.as_view(),
    #      name="change-email"),
    # path("change-email-verify/",  # Change email verification
    #      ChangeEmailVerifyAPIView.as_view(),
    #      name="change-email-verify"),
    path("change-password/",  # Change password for auth users
         ChangePasswordAPIView.as_view(),
         name="change-password"),

    # Tokens
    path("verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
