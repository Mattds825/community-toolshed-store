import uuid

from django.db import models
from django.db.models import Sum
from products.models import Item
from profiles.models import UserProfile

ORDER_ITEM_STATUS = (
    ('reserved', 'Reserved'),
    ('active', 'Currently Rented'),    
    ('returned', 'Returned'),    
)

PAYMENT_STATUS = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('failed', 'Failed'),
)

# Create your models here.

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    
    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        self.order_total = self.order_items.aggregate(Sum('item_total'))['item_total__sum'] or 0        
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.order_number
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, null=False, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(null=False)
    item_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    broken_amount = models.IntegerField(null=False, default=0)
    needs_cleaning = models.BooleanField(default=False)
    needs_repair = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=ORDER_ITEM_STATUS, default='reserved')
    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order item total
        and update the order total.        
        """
        self.item_total = self.item.price * self.quantity
        super().save(*args, **kwargs)        
        
    def __str__(self):
        return f'{self.item.name} on order {self.order.order_number}'
    
class Subscription(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions')
    subscription_number = models.CharField(max_length=32, null=False, editable=False)    
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=10)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=False)    
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    
    def _generate_sub_number(self):
        return uuid.uuid4().hex.upper()
    
    def __str__(self):
        return f"{self.user.username}_{self.end_date}"
    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.subscription_number:
            self.subscription_number = self._generate_sub_number()
        super().save(*args, **kwargs)