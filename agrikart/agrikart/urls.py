from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from farmer.views import FarmerViewSet
from buyer.views import CartViewSet
from buyer.views import CreateOrderFromCart, ConfirmOrder
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from farmer.views import ProduceViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="AgriKart API",
        default_version='v1',
        description="API documentation for AgriKart - Farmers & Buyers Platform",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@AgriKart.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'farmer', FarmerViewSet, basename='farmer')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'produce', ProduceViewSet, basename='produce')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('api.urls')),
    path('api/v1/buyer/', include('buyer.urls')),
    path('api/v1/farmer/', include('farmer.urls')),  # ✅ check/<phone_number>/ now works
    path('api/v1/logistics/', include('logistics.urls')),
    path('api/v1/orders/create-from-cart/', CreateOrderFromCart.as_view()),
    path('api/v1/orders/<int:pk>/confirm/', ConfirmOrder.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
