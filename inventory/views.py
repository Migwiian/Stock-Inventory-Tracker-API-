from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import InventoryItem
from .serializers import InventoryItemSerializer
# Create your views here.
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = InventoryItem.objects.filter(user=self.request.user)

        # Apply filters
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category__iexact=category) # Case-INsensitive

        price_min = self.request.query_params.get('price_min')
        if price_min is not None:
            try:
                queryset = queryset.filter(price__gte=float(price_min))
            except ValueError:
                # Ignore the filter if input is invalid
                pass

        price_max = self.request.query_params.get('price_max')
        if price_max is not None:
            try:
                queryset = queryset.filter(price__lte=float(price_max))
            except ValueError:
                pass

        low_stock_param = self.request.query_params.get('low_stock')
        if low_stock_param is not None:
            low_stock = low_stock_param.lower() in ['true', '1', 'yes']
            if low_stock:
                queryset = queryset.filter(quantity__lt=10)

        # Return the final, filtered queryset
        return queryset
    
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to add an item.")
        serializer.save(user=self.request.user) # Associate the item with the logged-in user on creation