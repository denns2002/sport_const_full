from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from mailings.models import Mailing


def send_email(email_subject, email_body, to_email) -> None:
    """
    Sends an email to a list of users. All mailings are stored in the database.

    :param str email_subject: message subject
    :param str email_body: message body
    :param str to_email: recipient list
    """
    from_email = settings.EMAIL_HOST_USER + settings.EMAIL_DOMAIN
    instance = Mailing.objects.create(is_error=False)

    try:
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            to=to_email,
            from_email=from_email
        )
        email.send()

    except Exception as error:
        instance.is_error = True
        instance.error = error

    finally:
        instance.subject = email_subject
        instance.body = email_body,
        instance.from_email = from_email

        users = get_user_model().objects.filter(email__in=to_email)
        for user in users:
            instance.recipients.add(user)
