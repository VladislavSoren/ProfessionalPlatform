from celery import shared_task
from mail_templated import send_mail


@shared_task
def notify_order_saved(order_pk, promocode):
    send_mail(
        "email/order-updated.html",
        {
            "order_pk": order_pk,
            "promocode": promocode,
        },
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
