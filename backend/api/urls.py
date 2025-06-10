from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerViewSet, BuyerViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import signup_view

router = DefaultRouter()
router.register(r'farmer', FarmerViewSet, basename='farmer')
router.register(r'buyer', BuyerViewSet, basename='buyer')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', obtain_auth_token),
    path('v1/auth/signup/', signup_view),
]
