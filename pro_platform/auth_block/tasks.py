from celery import shared_task
from django.contrib.auth.models import User
from mail_templated import send_mail


@shared_task
def welcome_user(user_pk):

    user: User = User.objects.get(pk=user_pk)

    send_mail(
        "email/reg_new.html",
        {
            "user": user,
        },
        "soren@admin.com",
        [user.email],
        fail_silently=False,
    )
