from rest_framework import serializers
from .models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'  # Include all fields from the model
        read_only_fields = ['id', 'date_added', 'last_updated', 'users']  # Make these fields read-only