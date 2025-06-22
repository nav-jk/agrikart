from django.urls import path
from .views import BuyerSignup, FarmerSignup
from .views import CustomTokenObtainPairView
from .views import MeView
from buyer.views import OrderReceiptView


urlpatterns = [
    path('signup/', BuyerSignup.as_view()),
    path('signup/farmer/', FarmerSignup.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()), 
     path("me/", MeView.as_view(), name="me"),
    path('orders/<int:order_id>/receipt/', OrderReceiptView.as_view(), name='order-receipt'),
]


from rest_framework.routers import DefaultRouter
from logistics.views import CourierAssignmentViewSet

router = DefaultRouter()
router.register(r'logistics/assignments', CourierAssignmentViewSet)

urlpatterns += router.urls
