from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop_projects.forms import DonatForm
from shop_projects.models import Donat


class DonatsListView(LoginRequiredMixin, ListView):
    queryset = (
        Donat
        .objects
        .filter(status=Donat.Status.AVAILABLE)
        .order_by("money")
        .select_related("user")
        .all()
    )

    extra_context = {
        "categories": queryset,
        "class_name": Donat._meta.object_name.lower(),
        "class_name_plural": Donat._meta.verbose_name_plural,
    }


class DonatDetailView(UserPassesTestMixin, DetailView):

    def test_func(self):
        return self.request.user.is_staff

    queryset = (
        Donat
        .objects
        .order_by("id")
        .select_related("user")
        .prefetch_related("projects")
        .all()
    )

    extra_context = {
        "categories": queryset,
        "class_name": Donat._meta.object_name.lower(),
        "class_name_plural": Donat._meta.verbose_name_plural,
        "back_url_to_all_objs": 'shop_projects:donats',
    }


class DonatCreateView(CreateView):
    model = Donat
    form_class = DonatForm
    success_url = reverse_lazy("shop_projects:donats")

    extra_context = {
        "class_name": Donat._meta.object_name.lower(),
        "class_name_plural": Donat._meta.verbose_name_plural,
    }


class DonatUpdateView(UpdateView):
    template_name_suffix = "_update_form"
    model = Donat
    form_class = DonatForm

    extra_context = {
        "class_name": Donat._meta.object_name.lower(),
        "class_name_plural": Donat._meta.verbose_name_plural,
    }

    def get_success_url(self):
        return reverse(
            "shop_projects:donat-details",
            kwargs={
                "pk": self.object.pk,
            }
        )


class DonatDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shop_projects.delete_donat"

    success_url = reverse_lazy("shop_projects:donats")
    queryset = (
        Donat
        .objects
        .filter(status=Donat.Status.AVAILABLE)
        .all()
    )

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.status = Donat.Status.ARCHIVED
        self.object.save()
        return redirect(success_url)


if __name__ == "__main__":
    print(DonatDetailView.mro())
