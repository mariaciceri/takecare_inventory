from django import forms
from django.core.validators import MinValueValidator
from .models import Order, OrderItem, Item


class OrderItemForm(forms.ModelForm):
    """
    Form for adding an item to an order.
    """
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form.
        """
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(quantity_in_stock__gt=0)
        self.fields['quantity'].validators = [MinValueValidator(1)]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user']

class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']
    