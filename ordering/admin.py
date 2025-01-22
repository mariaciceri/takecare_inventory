from django.contrib import admin, messages
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from .models import Order, Category, Item, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['item', 'quantity']
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'user')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username')
    ordering = ('status', 'created_at')
    inlines = [OrderItemInline]

    def get_readonly_fields(self, request, obj=None):
        """
        Makes all fields read-only.
        """
        if obj:
            return [field.name for field in self.model._meta.fields]
        return []
    
    def has_change_permission(self, request, obj=None):
        """
        Disables the change permission.
        """
        if obj:
            return False
        return True

    def approve_orders(self, request, queryset):
        """
        Approves the selected orders.
        """
        for order in queryset:
            try:
                if order.status == 0:
                    order.approve()
                    order.status = 1
                    order.save()
                    self.message_user(
                        request, f"Order {order.id} was approved."
                        )
                else:
                    self.message_user(
                        request,
                        f"Order {order.id} was already processed.",
                        level=messages.WARNING
                        )
            except Exception as e:
                self.message_user(
                    request,
                    f"Order {order.id} could not be approved: {e}",
                    level=messages.ERROR
                    )

    def reject_orders(self, request, queryset):
        """
        Rejects the selected orders.
        """
        for order in queryset:
            try:
                if order.status == 0:
                    order.status = 2
                    order.save()
                    self.message_user(
                        request, f"Order {order.id} was rejected."
                        )
                else:
                    self.message_user(
                        request,
                        f"Order {order.id} was already processed.",
                        level=messages.WARNING
                        )
            except Exception as e:
                self.message_user(
                    request,
                    f"Order {order.id} could not be rejected: {e}",
                    level=messages.ERROR
                    )
    
    actions = ['approve_orders', 'reject_orders']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'quantity_in_stock',
        'is_critical',
        'expiration_date',
        'low_stock_alert'
        )
    list_filter = ('category', 'expiration_date', 'is_critical')
    search_fields = ('name', 'category__name')
    ordering = ('quantity_in_stock', 'name')

    def low_stock_alert(self, obj):
        """
        Adds a 'Low Stock' warning for items with quantity below 100.
        """
        if obj.quantity_in_stock < 100:
            return format_html(
                '<span style="color: red; font-weight: bold;">Low Stock</span>'
                )
        return ""


admin.site.register(Category) 
admin.site.register(OrderItem)