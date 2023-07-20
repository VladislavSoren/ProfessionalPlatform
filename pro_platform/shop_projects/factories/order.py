import factory
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from factory.django import DjangoModelFactory

from shop_projects.models import OrderPaymentDetails, Order


class OrderPaymentDetailsFactory(DjangoModelFactory):
    class Meta:
        model = OrderPaymentDetails


@factory.django.mute_signals(post_save)
class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.Iterator(User.objects.all())
    # products = factory.Iterator(Product.objects.all())
    promocode = factory.Faker("word")
    # due to RelatedFactory OrderPaymentDetails will create ONLY AFTER Order creation
    payment_details = factory.RelatedFactory(
        OrderPaymentDetailsFactory,
        factory_related_name="order",
        # payed_at=factory.LazyFunction(datetime.utcnow)
        payed_at=factory.LazyFunction(timezone.now)
    )

    # ManyToManyField
    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for project in extracted:
                self.projects.add(project)

    # branches of creation by flags (Trait name = True)
    class Params:
        empty_promocode = factory.Trait(
            promocode="",
            payment_details=None,
        )
        paid = factory.Trait(
            payment_details__card_ends_with=factory.Faker("word"),
            payment_details__payed_at=factory.LazyFunction(timezone.now),
        )
        paid_confirmed = factory.Trait(
            payment_details__card_ends_with=factory.Faker("word"),
            payment_details__status=OrderPaymentDetails.Status.CONFIRMED,
            payment_details__payed_at=factory.LazyFunction(timezone.now),
        )


