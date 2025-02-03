from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import transaction
import datetime

STATUS = ((0, "Pending"), (1, "Approved"), (2, "Rejected"))

class CustomUser(AbstractUser):
    """
    Add approval to the user model.
    """
    is_approved = models.BooleanField(default=False)

class Order(models.Model):
    """
    Stores the order details of a user.
    """
    user = models.ForeignKey( 
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
        
    def approve(self):
        if self.status != 0:
            raise ValidationError("The order was already processed.")

        with transaction.atomic():
            for order_item in self.items.all():
                if order_item.quantity > order_item.item.quantity_in_stock:
                    raise ValidationError(
                        f"Insufficient stock for item {order_item.item.name}."
                    )
                order_item.item.quantity_in_stock -= order_item.quantity
                order_item.item.save()
    
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
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    def clean(self):
        """
        Validates the fields and if quantity is available in stock.
        """
        if not self.item_id or not self.order_id or self.quantity is None:
            raise ValidationError("All fields must be provided.")
        
        if self.quantity > self.item.quantity_in_stock:
            raise ValidationError(
                f"""The quantity must be less than or 
equal to the quantity in stock ({self.item.quantity_in_stock})."""
                )


    def __str__(self):
        return f"{self.quantity} {self.item.name}. Order: {self.order.id}"
    
