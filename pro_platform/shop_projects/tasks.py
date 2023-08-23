from celery import shared_task
from django.contrib.auth.models import User

from pro_platform.settings import EMAIL_ADMIN_ADDRESS

from django.core.mail import EmailMessage
from django.template.loader import get_template


@shared_task
def notify_order_saved(order_pk, promocode, user_pk, projects_info_dict):
    user: User = User.objects.get(pk=user_pk)

    # count total sum of order
    order_total_sum = sum(projects_info_dict.values())

    message = get_template("email/order_updated.html").render({
        "user": user,
        "order_pk": order_pk,
        "promocode": promocode,
        "projects_info_dict": projects_info_dict,
        "order_total_sum": order_total_sum,
    })
    mail = EmailMessage(
        subject="Order confirmation",
        body=message,
        from_email=EMAIL_ADMIN_ADDRESS,
        to=[user.email],
        reply_to=[EMAIL_ADMIN_ADDRESS],
    )
    mail.content_subtype = "html"
    mail.send()

    # write some task args for checking if the service is alive
    path_file = f'shop_projects/notifications/order_{order_pk}.txt'
    with open(path_file, 'w') as f:
        f.write(f'{order_pk},{promocode}, {projects_info_dict}')
