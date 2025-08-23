# inventory/models.py
from django.db import models
from django.conf import settings

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

# New model for logging inventory changes
class InventoryLog(models.Model):
    CHANGE_TYPES = [
        ('RESTOCK', 'Restock'),
        ('SALE', 'Sale'),
        ('ADJUSTMENT', 'Adjustment'),
        ('RETURN', 'Return'),
    ] # Define change types
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=50, choices=CHANGE_TYPES) # Type of change based on predefined choices
    quantity_changed = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.change_type} - {self.item.name} ({self.quantity_changed})"