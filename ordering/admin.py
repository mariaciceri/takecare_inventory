from django.contrib import admin
from django.utils.html import format_html
from .models import Order, Category, Item, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'user')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username')
    ordering = ('-created_at',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity_in_stock', 'is_critical', 'expiration_date', 'low_stock_alert')
    list_filter = ('category', 'expiration_date', 'is_critical')
    search_fields = ('name', 'category__name')
    ordering = ('quantity_in_stock', 'name')

    def low_stock_alert(self, obj):
        """
        Adds a 'Low Stock' warning for items with quantity below 100.
        """
        if obj.quantity_in_stock < 100:
            return format_html('<span style="color: red; font-weight: bold;">Low Stock</span>')
        return ""


admin.site.register(Category) 
admin.site.register(OrderItem) 
