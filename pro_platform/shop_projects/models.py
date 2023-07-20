from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import notify_order_saved


class BaseModel(models.Model):  # base class should subclass 'django.db.models.Model'

    class Status(models.IntegerChoices):
        ARCHIVED = 0
        AVAILABLE = 1

    status = models.IntegerField(
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    class Meta:
        abstract = True  # Set this model as Abstract


class Category(BaseModel):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# from shop_projects_app.models import Category
class Creator(BaseModel):
    class Meta:
        verbose_name_plural = "creators"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"Creator {self.user}"


class Project(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="projects_for_cats",  # Important  arg!
    )  # Если удалим Category, то Project не дропнится

    # new fields
    creator = models.ForeignKey(
        Creator,
        on_delete=models.PROTECT,
        null=True,
        related_name="projects_for_creators"
    )
    url = models.CharField(max_length=150, null=True)
    other_contributors = models.TextField(null=True)
    # archived = models.BooleanField(default=False)

    # Time fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product <№{self.id}, {self.name!r}>"


class Order(BaseModel):
    class Meta:
        verbose_name_plural = "orders"

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    projects = models.ManyToManyField(
        Project,
        related_name="orders",
    )
    promocode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderPaymentDetails(models.Model):
    class Meta:
        verbose_name_plural = "Order Payment Details"

    class Status(models.IntegerChoices):
        PENDING = 0
        CONFIRMED = 1

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment_details",
    )
    payed_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    card_ends_with = models.CharField(max_length=5, blank=True)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PENDING,
    )


# def on_order_create_add_payment_details
@receiver(post_save, sender=Order)
def on_order_save(instance: Order, created: bool, **kwargs):
    notify_order_saved.delay(
        order_pk=instance.pk,
        promocode=instance.promocode,
    )

    if not created:
        return

    # opd_obj = data from form

    OrderPaymentDetails.objects.get_or_create(
        order=instance,
        # card_ends_with='*369'
    )


class Donat(BaseModel):
    class Meta:
        verbose_name_plural = "donats"

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    projects = models.ManyToManyField(
        Project,
        related_name="donats",
        # on_delete=models.PROTECT,
    )
    money = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
