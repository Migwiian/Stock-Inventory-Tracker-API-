from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryLogViewSet

# This router will handle the main inventory endpoints like /api/inventory/
router = DefaultRouter()
router.register(r'inventory', InventoryItemViewSet, basename='inventory')

# These are the URL patterns for your API
urlpatterns = [
    # This includes all the standard CRUD endpoints from the router
    path('', include(router.urls)),
    
    # This manually defines the nested URL for the item history
    path('inventory/<int:item_pk>/history/', 
         InventoryLogViewSet.as_view({'get': 'list'}), 
         name='item-history'),
]