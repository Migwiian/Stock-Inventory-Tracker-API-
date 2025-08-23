from django.shortcuts import render
from rest_framework import viewsets
from .models import InventoryItem
from .serializers import InventoryItemSerializer
# Create your views here.
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

    def get_queryset(self):
        user = self.request.user 
        if user.is_authenticated: 
            return InventoryItem.objects.filter(users=user) # Ensure users only see their own items
        return InventoryItem.objects.none()
    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to add an item.")
        serializer.save(users=self.request.user) # Associate the item with the logged-in user