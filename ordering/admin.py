from django.contrib import admin, messages
from django.http import HttpRequest
from django.utils.html import format_html
from .models import CustomUser, Order, Category, Item, OrderItem
from django.forms import DateInput
import datetime

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
        'low_stock_alert',
        'close_exp_date'
        )
    list_filter = ('category', 'expiration_date', 'is_critical')
    search_fields = ('name', 'category__name')
    ordering = ('quantity_in_stock', 'name')

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Adds a date picker for the expiration date field.
        """
        if db_field.name == "expiration_date":
            kwargs['widget'] = DateInput(attrs={
                'type': 'date',
                'min': datetime.date.today() + datetime.timedelta(days=1),
                'class': 'date-field'
                })
        return super().formfield_for_dbfield(db_field, **kwargs)

    def low_stock_alert(self, obj):
        """
        Adds a 'Low Stock' warning for items with quantity below 100.
        """
        if obj.quantity_in_stock == 0:
            return format_html(
                '<span style="color: red; font-weight: bold;">Out of Stock</span>'
                )
        elif obj.quantity_in_stock < 100:
            return format_html(
                '<span style="color: orange; font-weight: bold;">Low Stock</span>'
                )
        
        return ""
    
    def close_exp_date(self, obj):
        """
        Adds a 'Close Expiration Date' warning for items with expiration date
        """
        if obj.expiration_date <= datetime.date.today():
            return format_html(
                '<span style="color: red; font-weight: bold;">Expired</span>'
                )
        elif obj.expiration_date < datetime.date.today() + datetime.timedelta(days=30):
            return format_html(
                '<span style="color: orange; font-weight: bold;">Close Expiration Date</span>'
                )
        return ""

    def has_module_permission(self, request):
        """
        Check for items expiring within 30 days, expired items, and low in stock
        """
        expiring_items = Item.objects.filter(
            expiration_date__lte=datetime.date.today() + datetime.timedelta(days=30),
            expiration_date__gt=datetime.date.today())
        expired_items = Item.objects.filter(expiration_date__lte=datetime.date.today())
        low_in_stock = Item.objects.filter(quantity_in_stock__lt=100)
        not_in_stock = Item.objects.filter(quantity_in_stock=0)

        if expiring_items.exists():
            message = f"{expiring_items.count()} item(s) are close to expiration!"
        
            storage = messages.get_messages(request)
            if message not in [msg.message for msg in storage]:
                self.message_user(request, message, level=messages.WARNING)

        if expired_items.exists():
            message = f"{expired_items.count()} item(s) have expired!"
        
            storage = messages.get_messages(request)
            if message not in [msg.message for msg in storage]:
                self.message_user(request, message, level=messages.ERROR)

        if low_in_stock.exists():
            message = f"{low_in_stock.count()} item(s) are low in stock!"
        
            storage = messages.get_messages(request)
            if message not in [msg.message for msg in storage]:
                self.message_user(request, message, level=messages.WARNING)

        if not_in_stock.exists():
            message = f"{not_in_stock.count()} item(s) are out of stock!"
        
            storage = messages.get_messages(request)
            if message not in [msg.message for msg in storage]:
                self.message_user(request, message, level=messages.ERROR)

        return super().has_module_permission(request)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('username', 'email')

    def has_module_permission(self, request):
        """
        Check for unapproved users and display a warning if any are found.
        """
        unapproved_users = CustomUser.objects.filter(is_approved=False)
        if unapproved_users.exists():
            message = f"{unapproved_users.count()} users are pending approval!"
        
            storage = messages.get_messages(request)
            if message not in [msg.message for msg in storage]:
                self.message_user(request, message, level=messages.WARNING)

        return super().has_module_permission(request)


admin.site.register(Category) 
admin.site.site_header = 'TakeCare System Administration'