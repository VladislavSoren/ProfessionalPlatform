from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Sum

from shop_projects.forms import OrderForm
from shop_projects.models import Order


@login_required
def order_list_view(request: HttpRequest) -> HttpResponse:
    query_orders = (
        Order
        .objects
        .filter(status=Order.Status.AVAILABLE)
        .order_by("id")
        .prefetch_related("user")
        .defer(
            "promocode",
            "created_at",
            "updated_at",
        )
        .all()
    )

    query_aggr_proj_sum = (
        Order
        .objects
        .filter(status=Order.Status.AVAILABLE)
        .order_by("id")
        .prefetch_related("projects")
        .values('id')
        .annotate(Sum('projects__price'))
    )

    query_list = zip(query_orders, query_aggr_proj_sum)

    return render(
        request=request,
        template_name="shop_projects/order_list.html",
        context={
            "query_list": query_list,
            "class_name": Order._meta.object_name.lower(),
            "class_name_plural": Order._meta.verbose_name_plural,
        }
    )


def is_staff_check(user):
    return user.is_staff


@user_passes_test(is_staff_check)
def order_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    queryset = (
        Order
        .objects
        .filter(id=pk)
        .prefetch_related("user", "projects")
        .all()
    )

    query_aggr_proj_sum = (
        Order
        .objects
        .filter(id=pk)
        .filter(status=Order.Status.AVAILABLE)
        .prefetch_related("projects")
        .values('id')
        .annotate(Sum('projects__price'))
    )

    query_list = zip(queryset, query_aggr_proj_sum)

    return render(
        request=request,
        template_name="shop_projects/order_detail.html",
        context={
            "query_list": query_list,
            "class_name": Order._meta.object_name.lower(),
            "class_name_plural": Order._meta.verbose_name_plural,
            "back_url_to_all_objs": 'shop_projects:orders',
            "pk": pk,
        }
    )


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("shop_projects:orders")

    extra_context = {
        "class_name": Order._meta.object_name.lower(),
        "class_name_plural": Order._meta.verbose_name_plural,
    }


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = "_update_form"
    model = Order
    form_class = OrderForm

    extra_context = {
        "class_name": Order._meta.object_name.lower(),
        "class_name_plural": Order._meta.verbose_name_plural,
    }

    def get_success_url(self):
        return reverse(
            "shop_projects:order-details",
            kwargs={
                "pk": self.object.pk,
            }
        )


class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shop_projects.delete_order"

    success_url = reverse_lazy("shop_projects:orders")
    queryset = (
        Order
        .objects
        .filter(status=Order.Status.AVAILABLE)
        .all()
    )

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.status = Order.Status.ARCHIVED
        self.object.save()
        return redirect(success_url)
