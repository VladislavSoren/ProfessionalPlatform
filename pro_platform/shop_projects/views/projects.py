from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop_projects.forms import ProjectForm
from shop_projects.models import Project


class ProjectsListView(ListView):
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

    extra_context = {
        "categories": queryset,
        "class_name": Project._meta.object_name.lower(),
        "class_name_plural": Project._meta.verbose_name_plural,
    }


class ProjectDetailView(DetailView):
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


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("shop_projects:projects")

    extra_context = {
        "class_name": Project._meta.object_name.lower(),
        "class_name_plural": Project._meta.verbose_name_plural,
    }


class ProjectUpdateView(UpdateView):
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


class ProjectDeleteView(DeleteView):
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
