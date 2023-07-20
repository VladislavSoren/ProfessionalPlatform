from django.contrib import admin

from .models import (
    Project,
    Category,
    Creator,
    OrderPaymentDetails,
    Order,
    Donat,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = "id", "name", "price", "category", "url", "creator", "status",
    list_display_links = "id", 'name',


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "id", "name", "description",
    list_display_links = "id", 'name',


@admin.register(Creator)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "id", "rating", "user",
    list_display_links = "id",


class PaymentDetailsInline(admin.TabularInline):
    model = OrderPaymentDetails


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        PaymentDetailsInline,
    ]
    list_display = "id", "user", "promocode", "created_at", "status"
    list_display_links = "id", "promocode"


@admin.register(OrderPaymentDetails)
class OrderPaymentDetailsAdmin(admin.ModelAdmin):
    list_display = "id", "payed_at", "card_ends_with", "status", "order"
    list_display_links = "id", "status"


@admin.register(Donat)
class CategoryDonat(admin.ModelAdmin):
    list_display = "id", "money", "created_at",
    list_display_links = "id",
