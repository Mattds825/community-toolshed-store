import uuid
from django.db import models
from products.models import Item, Tool
from checkout.models import Order

MAINTENANCE_STATUS = (
    ('pending', 'Pending'),    
    ('fixed', 'Written Off'),
    ('written_off', 'Written Off'),
)

# Create your models here.

class MaintenanceTicket(models.Model):
    ticket_number = models.CharField(max_length=32, null=False, editable=False)
    tool = models.ForeignKey(Tool, null=False, on_delete=models.CASCADE, related_name='maintenance_tickets')
    associated_order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE, related_name='maintenance_tickets')
    issue_description = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=12, choices=MAINTENANCE_STATUS, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()
    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.ticket_number:
            self.ticket_number = self._generate_order_number()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.ticket_number