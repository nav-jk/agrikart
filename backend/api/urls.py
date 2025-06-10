from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerViewSet, BuyerViewSet

router = DefaultRouter()
router.register(r'farmer', FarmerViewSet, basename='farmer')
router.register(r'buyer', BuyerViewSet, basename='buyer')

urlpatterns = [
    path('v1/', include(router.urls)),
]
