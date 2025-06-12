from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from farmer.models import Farmer
from buyer.models import Buyer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers import UserSerializer
from buyer.serializers import BuyerSerializer
from farmer.serializers import FarmerSerializer
from buyer.models import Buyer
from farmer.models import Farmer


class BuyerSignup(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            phone_number=data['phone_number'],
            is_buyer=True
        )
        Buyer.objects.create(user=user, address=data['address'])
        return Response({"msg": "Buyer created"}, status=201)

class FarmerSignup(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            phone_number=data['phone_number'],
            is_farmer=True
        )
        Farmer.objects.create(user=user, name=data['name'], address=data['address'])
        return Response({"msg": "Farmer created"}, status=201)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        response_data = {
            "user": {
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "is_farmer": user.is_farmer,
                "is_buyer": user.is_buyer,
            }
        }

        if user.is_buyer:
            try:
                buyer = Buyer.objects.get(user=user)
                response_data["buyer"] = BuyerSerializer(buyer).data
            except Buyer.DoesNotExist:
                response_data["buyer"] = None

        if user.is_farmer:
            try:
                farmer = Farmer.objects.get(user=user)
                response_data["farmer"] = FarmerSerializer(farmer).data
            except Farmer.DoesNotExist:
                response_data["farmer"] = None

        return Response(response_data)
