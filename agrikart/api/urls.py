from django.urls import path
from .views import BuyerSignup, FarmerSignup
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('signup/', BuyerSignup.as_view()),
    path('signup/farmer/', FarmerSignup.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()), 
]
