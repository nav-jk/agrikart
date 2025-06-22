from django.urls import path
from .views import NearbyOrdersView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourierAssignmentViewSet
from .views import AssignedOrdersView
from .views import UpdateOrderStatusView
from .views import OrderReceiptPDFView


router = DefaultRouter()
router.register(r'assignments', CourierAssignmentViewSet)


urlpatterns = [
    path('orders/nearby/', NearbyOrdersView.as_view(), name='nearby-orders'),
    path('', include(router.urls)),
    path('assigned-orders/', AssignedOrdersView.as_view(), name='assigned-orders'),
    path('orders/<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('orders/<int:order_id>/receipt/', OrderReceiptPDFView.as_view(), name='order-receipt-pdf'),
]
