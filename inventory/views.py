from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import InventoryItem, InventoryLog
from .serializers import InventoryItemSerializer, InventoryLogSerializer
from .filters import InventoryItemFilter
from .permissions import IsOwner
from rest_framework.pagination import PageNumberPagination

class IsOwner(permissions.BasePermission):
    ''' Custom permission to only allow owners of an object to access it. 
            Assumes the model instance has an `user` attribute.'''
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user # Only allow access if the object's user matches the request user

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = InventoryItemFilter
    ordering_fields = ['name', 'quantity', 'price', 'date_added']
    
    def get_queryset(self):
        """
        Returns the initial queryset for the authenticated user.
        Filtering is handled by the DjangoFilterBackend and filterset_class.
        """
        return InventoryItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Saves the new item and creates an initial inventory log entry.
        """
        new_item = serializer.save(user=self.request.user)
        InventoryLog.objects.create(
            item=new_item,
            user=self.request.user,
            change_type=InventoryLog.CHANGE_INITIAL,
            quantity_changed=new_item.quantity,
            notes="Initial stock added"
        )
    
    def perform_update(self, serializer):
        """
        Saves the updated item and logs the quantity change.
        """
        old_item = self.get_object()
        old_quantity = old_item.quantity
        updated_item = serializer.save()
        
        quantity_delta = updated_item.quantity - old_quantity
        
        if quantity_delta != 0:
            change_type = InventoryLog.CHANGE_RESTOCK if quantity_delta > 0 else InventoryLog.CHANGE_SALE
            InventoryLog.objects.create(
                item=updated_item,
                user=self.request.user,
                change_type=change_type,
                quantity_changed=abs(quantity_delta),
                notes=f"Quantity changed from {old_quantity} to {updated_item.quantity}"
            )

class InventoryLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['item', 'change_type']
    ordering_fields = ['timestamp']

    def get_queryset(self):
        """
        Returns the logs for the authenticated user.
        Filtering by 'item' and 'change_type' is handled by DjangoFilterBackend.
        """
        return InventoryLog.objects.filter(user=self.request.user)