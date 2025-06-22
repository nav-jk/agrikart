from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from farmer.views import FarmerViewSet
from .views import check_farmer_exists
from buyer.views import CartViewSet, CreateOrderFromCart, ConfirmOrder
from .views import ProducePricingListView

router = DefaultRouter()
router.register(r'farmer', FarmerViewSet, basename='farmer')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('api.urls')),
    path('api/v1/orders/create-from-cart/', CreateOrderFromCart.as_view()),
    path('api/v1/orders/<int:pk>/confirm/', ConfirmOrder.as_view()),
    path('check/<str:phone_number>/', check_farmer_exists, name='check_farmer_exists'),
    path('produce/prices/', ProducePricingListView.as_view(), name='produce-prices'),
]
