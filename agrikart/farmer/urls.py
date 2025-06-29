from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from farmer.views import FarmerViewSet
from buyer.views import CartViewSet, CreateOrderFromCart, ConfirmOrder

router = DefaultRouter()
router.register(r'farmer', FarmerViewSet, basename='farmer')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('api.urls')),
    path('api/v1/orders/create-from-cart/', CreateOrderFromCart.as_view()),
    path('api/v1/orders/<int:pk>/confirm/', ConfirmOrder.as_view()),
]
