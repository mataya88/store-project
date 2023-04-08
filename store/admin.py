from django.contrib import admin, messages
from django.db.models import Count, Value
from django.db.models.functions import Concat
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
    # form lists
    # fields=[('title','slug'),'category','last_update'] # fields in add form
    # exclude = ['description'] # excluded fields in form
    # readonly_fields=['last_update'] # auto fields must be readonly
    # fieldsets = [
    #     (None, {
    #             'fields': ['title', 'slug']
    #             }),
    #     ('Category',{
    #             'fields':('category',)
    #     })]

    # if you want a field not to be required in the form, make its blank=True in models.py
    prepopulated_fields = {
        'slug':['title']
    }
    autocomplete_fields = ['category']

    # data lists
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
    list_display = ['name','featured_product_title', 'count_product']
    list_select_related = ['featured_product']
    search_fields = ['name']

    @admin.display(ordering='count_product', description='products')
    def count_product(self, category: models.Category):
        # using format_html to add a link to the filed value
        # reverse is used to generate the url dynamically
        # reverse('admin:appname_model_pagetype')
        url = (reverse('admin:store_product_changelist')
                +'?'
                + urlencode({'category_id':str(category.id)}))
        return format_html('<a href={}>{}</a>',url,category.count_product)

    @admin.display(ordering="featured_product__title")
    def featured_product_title(self,category):
        try:
            return category.featured_product.title
        except AttributeError:
            return None

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
                                    count_product=Count('product'))

    


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'birth_date', 'membership',
                    'total_orders']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith',
                     'last_name__istartswith', 'birth_date', 'membership']
    search_help_text = 'format for date is YYYY-MM-DD'

    ordering = ['first_name', 'last_name']

    @admin.display(ordering='total_orders')
    def total_orders(self,customer):
        url = (reverse('admin:store_order_changelist')
                +'?'
                + urlencode({'customer_id':str(customer.id)}))
        return format_html('<a href={}>{}</a>',url,customer.total_orders)

    def get_queryset(self, request):
        return (super().get_queryset(request)
                    .annotate(total_orders=Count('order__id')))


class OrderItemInline(admin.TabularInline): # you can use StackedInline instead

    # class to add orderitems in the order admin form
    model = models.OrderItem
    extra = 0 # number of rows displayed be default
    min_num = 1 # minimum allowed childs
    max_num = 3 # maximum allowed childs
    fk_name = 'order'


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

    list_display = ['id','placed_at',
                    'payment_status', 'customer_name']
    list_per_page = 10
    list_select_related = ['customer']
    search_fields = ['placed_at']


    @admin.display(
        ordering=Concat("customer__first_name",
                         Value(" "),
                         "customer__last_name"),
        description="customer")
    def customer_name(self, order):
        
        return order.customer.first_name + ' ' + order.customer.last_name

    
