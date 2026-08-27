import secrets
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def generate_verification_code():
    num = secrets.randbelow(1000000)
    code = str(num)
    while len(code) < 6:
        code = "0" + code
    return code


def send_verification_code_email(user, code):
    html_content = render_to_string(
        "emails/verification_code.html",
        {"code": code},
    )

    email = EmailMultiAlternatives(
        subject="ISAS — Email Verification",
        body=f"Your verification code is {code}. The code is valid for 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
