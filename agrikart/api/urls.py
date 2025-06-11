from django.urls import path
from .views import BuyerSignup, FarmerSignup
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('signup/', BuyerSignup.as_view()),
    path('signup/farmer/', FarmerSignup.as_view()),
    path('token/', TokenObtainPairView.as_view()),
]
