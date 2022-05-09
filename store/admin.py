from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
from django.db.models import Count
# Use "register" to add the desired models into the admin page
# Add collection


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


admin.site.register(models.Collection, CollectionAdmin)

# Add Product using class instead of "register"


class ProductAdmin(admin.ModelAdmin):
    # here I can choose the options to show
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    # this is needed to preload the collection data to avoid that for each product there will be a call to the db when looking at colleciton title of the product
    list_select_related = ['collection']


# Define a particular show option field for the product Model in the admin

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    def collection_title(self, product):
        return product.collection.title  # this works however for each product there will be a new query on the db for the colletion, to avoid this we need to preload the collection by using list_selected_related


admin.site.register(models.Product, ProductAdmin)

# Add the order model in the admin page


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'placed_at']


admin.site.register(models.Order, OrderAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name',
                    'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': customer.pk
            }))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


admin.site.register(models.Customer, CustomerAdmin)
