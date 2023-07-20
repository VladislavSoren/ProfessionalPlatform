from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.index import ShopIndexView, get_task_info
from .views.projects import (
    ProjectsListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
)
from .views.categories import (
    CategoriesListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)
from .views.creators import (
    CreatorsListView,
    CreatorDetailView,
    CreatorCreateView,
    CreatorUpdateView,
    CreatorDeleteView,
)

from .views.donats import (
    DonatsListView,
    DonatDetailView,
    DonatCreateView,
    DonatUpdateView,
    DonatDeleteView,
)
from .views.orders import (
    order_list_view,
    order_detail_view,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
)

app_name = "shop_projects"

urlpatterns = [
    path('', ShopIndexView.as_view(), name="index"),
    path("orders/task/<task_id>/", get_task_info, name="get-order-task-id"),

    path('projects', ProjectsListView.as_view(), name="projects"),
    path("projects/create/", ProjectCreateView.as_view(), name="create-project"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-details"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="update-project"),
    path("projects/<int:pk>/confirm-delete/", ProjectDeleteView.as_view(), name="confirm-delete-project"),

    path('categories', CategoriesListView.as_view(), name="categories"),
    path("categories/create/", CategoryCreateView.as_view(), name="create-category"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-details"),
    path("categories/<int:pk>/update/", CategoryUpdateView.as_view(), name="update-category"),
    path("categories/<int:pk>/confirm-delete/", CategoryDeleteView.as_view(), name="confirm-delete-category"),

    path('creators', CreatorsListView.as_view(), name="creators"),
    path("creators/create/", CreatorCreateView.as_view(), name="create-creator"),
    path("creators/<int:pk>/", CreatorDetailView.as_view(), name="creator-details"),
    path("creators/<int:pk>/update/", CreatorUpdateView.as_view(), name="update-creator"),
    path("creators/<int:pk>/confirm-delete/", CreatorDeleteView.as_view(), name="confirm-delete-creator"),

    path('donats', DonatsListView.as_view(), name="donats"),
    path("donats/create/", DonatCreateView.as_view(), name="create-donat"),
    path("donats/<int:pk>/", DonatDetailView.as_view(), name="donat-details"),
    path("donats/<int:pk>/update/", DonatUpdateView.as_view(), name="update-donat"),
    path("donats/<int:pk>/confirm-delete/", DonatDeleteView.as_view(), name="confirm-delete-donat"),

    path('orders', order_list_view, name="orders"),
    path("orders/create/", OrderCreateView.as_view(), name="create-order"),
    path("orders/<int:pk>/", order_detail_view, name="order-details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="update-order"),
    path("orders/<int:pk>/confirm-delete/", OrderDeleteView.as_view(), name="confirm-delete-order"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
