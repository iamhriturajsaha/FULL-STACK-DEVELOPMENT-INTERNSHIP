"""
NOVA/FORM — Django Admin Configuration

Rich admin interface for managing products, orders, and categories.
"""

from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'product_name', 'price', 'quantity', 'subtotal']
    extra = 0
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'compare_at_price',
        'stock_quantity', 'featured', 'new_arrival', 'created_at'
    ]
    list_filter = ['category', 'featured', 'new_arrival', 'created_at']
    list_editable = ['price', 'stock_quantity', 'featured', 'new_arrival']
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_at_price')
        }),
        ('Images', {
            'fields': ('image', 'secondary_image')
        }),
        ('Inventory', {
            'fields': ('stock_quantity',)
        }),
        ('Flags', {
            'fields': ('featured', 'new_arrival')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'full_name', 'email', 'total',
        'status', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'full_name', 'email']
    readonly_fields = [
        'order_number', 'user', 'subtotal', 'shipping', 'total', 'created_at'
    ]
    inlines = [OrderItemInline]
    list_editable = ['status']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'status', 'created_at')
        }),
        ('Customer', {
            'fields': ('full_name', 'email')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Totals', {
            'fields': ('subtotal', 'shipping', 'total')
        }),
    )


# Customize admin site
admin.site.site_header = 'NOVA/FORM Administration'
admin.site.site_title = 'NOVA/FORM Admin'
admin.site.index_title = 'Store Management'
