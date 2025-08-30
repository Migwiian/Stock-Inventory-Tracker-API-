from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import InventoryItem, InventoryLog
from .serializers import InventoryItemSerializer, InventoryLogSerializer
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'quantity', 'price', 'date_added']
    
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
        serializer.save(user=self.request.user) # Associate the item with the logged-in user on creation
        new_item = serializer.instance # Capture the newly created item
        InventoryLog.objects.create( # This logs the creation as a restock
            item=new_item,
            user=self.request.user,
            change_type= InventoryLog.CHANGE_INITIAL,
            quantity_changed=new_item.quantity,
            notes="Initial stock added"
        )
    def perform_update(self, serializer):
        old_item = self.get_object()
        old_quantity = old_item.quantity
        updated_item = serializer.save()
        quantity_delta = updated_item.quantity - old_quantity
        if quantity_delta != 0:
            if quantity_delta > 0:
                change_type = InventoryLog.CHANGE_RESTOCK
            else:
                change_type = InventoryLog.CHANGE_SALE
            InventoryLog.objects.create(
                item=updated_item,
                user=self.request.user,
                change_type=change_type,
                quantity_changed=quantity_delta,
                notes=f"Quantity changed from {old_quantity} to {updated_item.quantity}"
            )
class InventoryLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter logs to only those of the logged-in user, that is, the user making the request
        queryset = InventoryLog.objects.filter(user=self.request.user)
        item_id = self.kwargs.get('item_pk')
        if item_id:
            queryset = queryset.filter(item__id=item_id)
        # Additional filtering that ensures only logs for a specific item if 'item_id' is provided as a query parameter
        query_item_id = self.request.query_params.get('item_id')
        if query_item_id:
            queryset = queryset.filter(item__id=query_item_id)
        return queryset