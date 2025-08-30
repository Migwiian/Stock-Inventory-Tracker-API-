from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include

from .views import InventoryItemViewSet, InventoryLogViewSet

# This is the primary router for the top-level endpoints
router = DefaultRouter()
router.register(r'inventory', InventoryItemViewSet, basename='inventory')

# This is the nested router for the history logs related to a specific item
inventory_router = routers.NestedSimpleRouter(router, r'inventory', lookup='inventory')
inventory_router.register(r'history', InventoryLogViewSet, basename='inventory-history')

urlpatterns = [
    # This includes the URLs from both the main and nested routers
    path('', include(router.urls)),
    path('', include(inventory_router.urls)),
]