from celery import shared_task

from django.core.management import call_command
from apps.users.models import User
from apps.users.utils import send_verification_code_email


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def send_verification_email(user_id, code):
    user = User.objects.get(pk=user_id)
    send_verification_code_email(user, code)


@shared_task
def clear_expired_sessions():
    call_command("clearsessions")
