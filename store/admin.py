from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models
from django.db.models import Count

class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset) :
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # get current admin url
        # reverse('admin:<app>_<model>_<page>')
        url = f'{reverse("admin:store_product_changelist")}?{urlencode({"collection__id":str(collection.id)})}'
        return format_html(f'<a href={url}>{collection.products_count}</a>')
    
    def get_queryset(self, request:HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count('product'))


# alternative way of register a mode via a decorator with a class that is used to 
# customize hos the Product List looks
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection'] # this is used to minimize hitting the db too much when using collection_title method
    list_filter = ['collection', 'last_update', InventoryFilter]
    actions = ['clear_inventory']  # customize options in actions dropdown
    search_fields = ['title']

    # customize data entry forms for the models
    # fields= ['title', 'slug'] # show only title and slug
    # exclude = ['promotions'] # do not show promotions in the form
    # readonly_fields=['unit_price'] # make unit_price readonly
    prepopulated_fields = {'slug': ['title']} # populate slug field with title
    autocomplete_fields=['collection']

    # Add a computed field for inventory to display a string like low etc.
    # also add sorting to this computed filed using "admin.display" decorator
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset:QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated.', messages.ERROR)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name', 'last_name', 'membership', 'orders_count']
    list_editable=['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = f'{reverse("admin:store_order_changelist")}?{urlencode({"customer__id":str(customer.id)})}'
        return format_html(f'<a href={url}>{customer.orders_count}</a>')
    
    def get_queryset(self, request:HttpRequest):
        return super().get_queryset(request).annotate(orders_count=Count('order'))

# note we can have also "admin.StackedInline" where each sub/child item appears as a seperate form
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields=['product']
    min_num = 1
    extra = 0 # hide place holders that is empty rows that appear ready to be filled

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=['id', 'placed_at', 'customer']
    autocomplete_fields=['customer']
    inlines = [OrderItemInline]
      