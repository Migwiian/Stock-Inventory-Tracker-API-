from django_filters.rest_framework import NumberFilter, BooleanFilter, FilterSet
from .models import InventoryItem

class InventoryItemFilter(FilterSet):
    '''This class defines how we want to filter for the API'''
    # Filter for min price: api/items/?price_min=50
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    # Filter for max price: api/items/?price_max=100
    price_max = NumberFilter(field_name='price', lookup_expr='lte')
    # Filter for low stock: api/items/?low_stock=true
    low_stock = BooleanFilter(method='filter_low_stock')

    def filter_low_stock(self, queryset, name, value):
        """
        Custom method to handle low stock filtering.
        If low_stock=true, show only items with less than 10 in stock.
        """
        if value:
            return queryset.filter(quantity__lt=10)
        return queryset
    
    class Meta:
        model = InventoryItem
        fields = ['category']