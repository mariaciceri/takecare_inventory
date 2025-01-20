from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime

STATUS = ((0, "Pending"), (1, "Approved"), (2, "Rejected"))


class Order(models.Model):
    """
    Stores the order details of a user.
    """
    user = models.ForeignKey( 
        User, on_delete=models.CASCADE, related_name='orders'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    total_amount_items = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class Category(models.Model):
    """
    Stores the category of an item.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
        
    def __str__(self):
        return f"Category: {self.name}"
    
class Item(models.Model):
    """
    Stores the details of an item.
    """
    def expiration_date_validator(value):
        """
        Validates the expiration date of an item.
        """
        if value <= datetime.date.today():
            raise ValidationError(
                "The expiration date must be in the future."
                )
        
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='items'
    )
    expiration_date = models.DateField(
        validators=[expiration_date_validator]
        )
    is_critical = models.BooleanField(default=False)
    quantity_in_stock = models.PositiveIntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class OrderItem(models.Model):
    """ 
    Stores the items in an order.
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='order_items'
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
