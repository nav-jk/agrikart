from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerViewSet, BuyerViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import signup_view
from .views import farmer_signup_view
from .views import add_to_cart, create_order_from_cart
from .views import CartItemDetailView
from .views import confirm_order_payment

router = DefaultRouter()
router.register(r'farmer', FarmerViewSet, basename='farmer')
router.register(r'buyer', BuyerViewSet, basename='buyer')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', obtain_auth_token),
    path('v1/auth/signup/', signup_view),
    path('auth/signup/farmer/', farmer_signup_view),
    path('cart/', add_to_cart, name='add-to-cart'),
    path('cart/<int:pk>/', CartItemDetailView.as_view(), name='cart-detail'),
    path('orders/<int:order_id>/confirm/', confirm_order_payment, name='confirm-order'),
]
