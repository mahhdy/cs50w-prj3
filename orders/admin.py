from django.contrib import admin
from django import forms
from .models import *

# Register your models here.


def make_ready(modeladmin, request, queryset):
    queryset.update(status='ready')


make_ready.short_description = "Mark selected orders as ready"
make_ready.allowed_permissions = ('change',)


def make_completed(modeladmin, request, queryset):
    queryset.update(status='completed')


make_completed.short_description = "Mark selected orders as completed"
make_completed.allowed_permissions = ('change',)


class Order_detailAdmin(admin.ModelAdmin):
    pass


class OrderInline(admin.TabularInline):
    model = Order_detail
    readonly_fields = ('item_total',)
    fieldsets = [
        (None, {'fields': ['food', 'toppings',
                           'quantity', 'item_total', 'extra', ]}),
    ]
    extra=0


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_type', 'size', 'price',)
    list_filter = ('food_type', 'size', 'name', 'price',)
    search_fields = ('name', 'size',)
    ordering = ('food_type', 'name', '-size',)


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInline, ]
    date_hierarchy = ('date_added')
    list_display = ('customer', 'chef', 'date_added',
                    'order_total', 'confirmed', 'status',)
    list_filter = ('customer', 'chef', 'confirmed', 'status',
                   'date_added', 'order_details__food__food_type__name')
    list_editable = ('confirmed', 'status', 'chef')
    search_fields = ('customer', 'note', 'order_details__food__name')
    ordering = ('-date_added', 'confirmed', 'status',)
    actions = [make_ready, make_completed]


admin.site.register(Topping)
admin.site.register(Food, FoodAdmin)
admin.site.register(Food_type)
admin.site.register(Order, OrderAdmin)
