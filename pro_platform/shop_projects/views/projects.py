from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop_projects.forms import ProjectForm
from shop_projects.models import Project, Creator
from shop_projects.views.checking_relations import user_is_creator, project_belongs_creator


class ProjectsListView(LoginRequiredMixin, ListView):
    queryset = (
        Project
        .objects
        .filter(status=Project.Status.AVAILABLE)
        .order_by("id")
        .select_related("category")
        .defer(
            "description",
            "created_at",
            "updated_at",
            "category__description",
        )
        .all()
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = self.queryset
        context["class_name"] = Project._meta.object_name.lower()
        context["class_name_plural"] = Project._meta.verbose_name_plural
        context["is_creator"] = user_is_creator(self)

        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    queryset = (
        Project
        .objects
        .order_by("id")
        .select_related("creator")
        .prefetch_related("donats", "donats__user")
        .all()
    )

    extra_context = {
        "categories": queryset,
        "class_name": Project._meta.object_name.lower(),
        "class_name_plural": Project._meta.verbose_name_plural,
        "back_url_to_all_objs": 'shop_projects:projects',
    }


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    # access only for creators (top-level protection)
    def test_func(self):
        return user_is_creator(self)

    model = Project
    # fields = ["name"]
    form_class = ProjectForm
    success_url = reverse_lazy("shop_projects:projects")

    extra_context = {
        "class_name": Project._meta.object_name.lower(),
        "class_name_plural": Project._meta.verbose_name_plural,
    }

    # if user is not creator -> return form_invalid (low-level protection)
    def form_valid(self, form):

        try:
            form.instance.creator = self.request.user.creator
        except ObjectDoesNotExist:
            return super().form_invalid(form)
        else:
            return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    def test_func(self):
        return user_is_creator(self) and project_belongs_creator(self)

    template_name_suffix = "_update_form"
    model = Project
    form_class = ProjectForm

    extra_context = {
        "class_name": Project._meta.object_name.lower(),
        "class_name_plural": Project._meta.verbose_name_plural,
    }

    def get_success_url(self):
        return reverse(
            "shop_projects:project-details",
            kwargs={
                "pk": self.object.pk,
            }
        )


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "shop_projects.delete_project"

    success_url = reverse_lazy("shop_projects:projects")
    queryset = (
        Project
        .objects
        .filter(status=Project.Status.AVAILABLE)
        .all()
    )

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.status = Project.Status.ARCHIVED
        self.object.save()
        return redirect(success_url)
