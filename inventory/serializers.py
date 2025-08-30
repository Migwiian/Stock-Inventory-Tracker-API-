from rest_framework import serializers
from .models import InventoryItem  # Only import what is needed at the top level

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        # CORRECTION: The field name is 'user', not 'users'
        read_only_fields = ['id', 'date_added', 'last_updated', 'user']


class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        # Import the model here to avoid circular imports
        from .models import InventoryLog
        model = InventoryLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'user', 'item', 'change_type', 'quantity_changed']