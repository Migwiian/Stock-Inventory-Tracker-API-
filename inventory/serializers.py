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
    def validate(self, data):
        change_type = data.get('change_type')
        quantity_changed = data.get('quantity_changed')
        '''In simple terms, sales reduce stock, restocks increase it, and initial stock sets it.'''
        if change_type is not None and quantity_changed is not None:
            if change_type == InventoryLog.CHANGE_SALE and quantity_changed > 0:
                raise serializers.ValidationError({"quantity_changed": "For sales, quantity_changed must be negative."})
            if change_type == InventoryLog.CHANGE_RESTOCK and quantity_changed < 0:
                raise serializers.ValidationError({"quantity_changed": "For restocks, quantity_changed must be positive."})
            if change_type == InventoryLog.CHANGE_INITIAL and quantity_changed < 0:
                raise serializers.ValidationError({"quantity_changed": "For initial stock, quantity_changed must be positive."})
        
        return data 
