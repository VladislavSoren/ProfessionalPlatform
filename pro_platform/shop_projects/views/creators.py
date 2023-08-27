from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop_projects.forms import CreatorForm
from shop_projects.models import Creator
from shop_projects.views.checking_relations import user_is_creator, creator_belongs_user


class CreatorsListView(LoginRequiredMixin, ListView):
    queryset = (
        Creator
        .objects
        .filter(status=Creator.Status.AVAILABLE)
        .select_related("user")
        .order_by("id")
        .all()
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = self.queryset
        context["class_name"] = Creator._meta.object_name.lower()
        context["class_name_plural"] = Creator._meta.verbose_name_plural
        context["is_creator"] = user_is_creator(self)

        return context


class CreatorDetailView(LoginRequiredMixin, DetailView):
    queryset = (
        Creator
        .objects
        .order_by("id")
        .select_related("user")
        .prefetch_related("projects_for_creators")
        .all()
    )

    extra_context = {
        "categories": queryset,
        "class_name": Creator._meta.object_name.lower(),
        "class_name_plural": Creator._meta.verbose_name_plural,
        "back_url_to_all_objs": 'shop_projects:creators',
    }


class CreatorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    # access in user in NOT creator
    def test_func(self):
        return not user_is_creator(self)

    model = Creator
    form_class = CreatorForm
    success_url = reverse_lazy("shop_projects:creators")

    extra_context = {
        "class_name": Creator._meta.object_name.lower(),
        "class_name_plural": Creator._meta.verbose_name_plural,
    }

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class CreatorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    def test_func(self):
        return user_is_creator(self) and creator_belongs_user(self)

    template_name_suffix = "_update_form"
    model = Creator
    form_class = CreatorForm

    extra_context = {
        "class_name": Creator._meta.object_name.lower(),
        "class_name_plural": Creator._meta.verbose_name_plural,
    }

    def get_success_url(self):
        return reverse(
            "shop_projects:creator-details",
            kwargs={
                "pk": self.object.pk,
            }
        )


class CreatorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "shop_projects.delete_creator"

    success_url = reverse_lazy("shop_projects:creators")
    queryset = (
        Creator
        .objects
        .filter(status=Creator.Status.AVAILABLE)
        .all()
    )

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.status = Creator.Status.ARCHIVED
        self.object.save()
        return redirect(success_url)
