from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include

from .views import InventoryItemViewSet, InventoryLogViewSet

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet)   
router.register(r'logs', InventoryLogViewSet, basename='inventorylog')

urlpatterns = [
    path('', include(router.urls)),
]