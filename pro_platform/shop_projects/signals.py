from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from shop_projects.models import Order, OrderPaymentDetails
from shop_projects.tasks import notify_order_saved


# def on_order_create_add_payment_details
@receiver(post_save, sender=Order)
def on_order_save(instance: Order, created: bool, **kwargs):
    if not created:
        return

    OrderPaymentDetails.objects.get_or_create(
        order=instance,
    )


@receiver(m2m_changed, sender=Order.projects.through)
def cart_update_total_when_item_added(sender, instance, action, *args, **kwargs):
    if action == 'post_add':
        projects_info_dict = {project.name: project.price for project in instance.projects.all()}

        notify_order_saved.delay(
            order_pk=instance.pk,
            promocode=instance.promocode,
            user_pk=instance.user.id,
            projects_info_dict=projects_info_dict,
        )
