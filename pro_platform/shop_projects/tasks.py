from celery import shared_task
from mail_templated import send_mail

from pro_platform.settings import EMAIL_ADMIN_ADDRESS


@shared_task
def notify_order_saved(order_pk, promocode, user_email):
    send_mail(
        "email/order-updated.html",
        {
            "order_pk": order_pk,
            "promocode": promocode,
        },
        EMAIL_ADMIN_ADDRESS,
        [user_email],
        fail_silently=False,
    )
