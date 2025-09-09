from rest_framework import serializers
from .models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ['id', 'date_added', 'last_updated', 'user']
    def validate_quantity(self, value):
        ''' Ensure quantity is non-negative '''
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import InventoryLog
        model = InventoryLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'user', 'item', 'change_type', 'quantity_changed']
    def validate_quantity_changed(self, data):
        change_type = data[change_type]
        quantity_changed = data[quantity_changed, 0]
        ''' Validation rules based on change type 
         - Sales must have negative quantity_changed
         - Restocks must have positive quantity_changed
         - Initial stock must have positive quantity_changed
         - Returns must have positive quantity_changed
         - Adjustments can be positive or negative but not zero
         '''
        if change_type == InventoryLog.CHANGE_SALE and quantity_changed > 0:
            raise serializers.ValidationError("For sales, quantity_changed must be negative.")
        if change_type in InventoryLog.CHANGE_RESTOCK and quantity_changed < 0:
            raise serializers.ValidationError("For restocks, quantity_changed must be positive.")
        if change_type == InventoryLog.CHANGE_INITIAL and quantity_changed < 0:
            raise serializers.ValidationError("For initial stock, quantity_changed must be positive.")
        if change_type == InventoryLog.CHANGE_RETURN and quantity_changed < 0:
            raise serializers.ValidationError("For returns, quantity_changed must be positive.")
        if change_type == InventoryLog.CHANGE_ADJUSTMENT and quantity_changed == 0:
            raise serializers.ValidationError("For adjustments, quantity_changed cannot be zero.")
        return data
