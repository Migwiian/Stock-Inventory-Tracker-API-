from rest_framework import serializers
from .models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'  # Include all fields from the model
        read_only_fields = ['id', 'date_added', 'last_updated', 'users']  # Make these fields read-only
class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'user', 'item', 'change_type', 'quantity_changed']  # Make these fields read-only    