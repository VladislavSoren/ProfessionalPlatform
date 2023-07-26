from celery import shared_task
from django.contrib.auth.models import User
from mail_templated import send_mail

from pro_platform.settings import EMAIL_ADMIN_ADDRESS


@shared_task
def welcome_user(user_pk):

    user: User = User.objects.get(pk=user_pk)

    send_mail(
        "email/reg_new.html",
        {
            "user": user,
        },
        EMAIL_ADMIN_ADDRESS,
        [user.email],
        fail_silently=False,
    )
