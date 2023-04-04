from django.contrib import admin, messages
from django.db.models import Count
from . import models
from django.urls import reverse
from django.utils.html import format_html, urlencode
# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    # custom filter for product admin
    title = 'inventory status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),  # first is url query param, second is human readable
            ('>=10', 'Good')
        ]

    def queryset(self, request, queryset):
        # self.value() is the url query parameter
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>=10':
            return queryset.filter(inventory__gte=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    fields=[('title','slug'),'category','last_update'] # fields in add form
    readonly_fields=['last_update'] # auto fields must be readonly
    list_display = ['title', 'unit_price', 'inventory',
                    'inventory_status', 'category_name', 'featured_product']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['inventory', 'unit_price']
    list_filter = ['last_update', 'category__name', InventoryFilter]
    actions=['clear_inventory']

    @admin.display(ordering='inventory')
    def inventory_status(self, product: models.Product):
        # custom field
        if product.inventory < 10:
            return 'Low'
        else:
            return 'Good'

    @admin.display(ordering='category__name')
    def category_name(self, product):
        return product.category.name

    @admin.display(ordering='category__featured_product', boolean=True)
    def featured_product(self, product):
        return id == product.category.featured_product

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        # action to clear the inventory of selected rows
        num_updated = queryset.update(inventory=0)
        self.message_user(request,
                f'{num_updated} products has been updated successfully',
                messages.ERROR)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'count_product']

    @admin.display(ordering='count_product', description='products')
    def count_product(self, category: models.Category):
        # using format_html to add a link to the filed value
        # reverse is used to generate the url dynamically
        # reverse('admin:appname_model_pagetype')
        url = (reverse('admin:store_product_changelist')
                +'?'
                + urlencode({'category_id':str(category.id)}))
        return format_html('<a href={}>{}</a>',url,category.count_product)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(count_product=Count('product'))

    


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'birth_date', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith',
                     'last_name__istartswith', 'birth_date', 'membership']
    search_help_text = 'format for date is YYYY-MM-DD'

    ordering = ['first_name', 'last_name']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'payment_status', 'customer_name']
    list_per_page = 10
    list_select_related = ['customer']
    search_fields = ['placed_at']

    @admin.display(ordering="customer__first_name", description="customer")
    def customer_name(self, order):
        return order.customer.first_name + ' ' + order.customer.last_name
