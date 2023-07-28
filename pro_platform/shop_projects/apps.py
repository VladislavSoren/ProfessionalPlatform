from django.apps import AppConfig


class ShopProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shop_projects"

    def ready(self):
        from shop_projects import signals
