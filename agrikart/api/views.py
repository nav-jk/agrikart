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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from buyer.models import Buyer, Order
from buyer.serializers import BuyerSerializer, OrderSerializer
from farmer.models import Farmer
from farmer.serializers import FarmerSerializer
from django.conf import settings


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
        print(f"🧾 MeView accessed by user: {user.username}, is_buyer={user.is_buyer}, is_farmer={user.is_farmer}")

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

                # ✅ Fetch orders placed by this buyer
                orders = Order.objects.filter(buyer=buyer).order_by("-created_at")
                print(f"📦 Found {orders.count()} orders for buyer {buyer}")

                order_list = []
                for order in orders:
                    order_data = OrderSerializer(order).data
                    receipt_url = f"{settings.DOMAIN}/api/v1/auth/orders/{order.id}/receipt/"
                    order_data["receipt_pdf_url"] = receipt_url
                    order_list.append(order_data)
                    print(f"🧾 Added order #{order.id} with receipt {receipt_url}")

                response_data["buyer"]["orders"] = order_list

            except Buyer.DoesNotExist:
                print("❌ Buyer profile not found for user")
                response_data["buyer"] = None

        if user.is_farmer:
            try:
                farmer = Farmer.objects.get(user=user)
                response_data["farmer"] = FarmerSerializer(farmer).data
            except Farmer.DoesNotExist:
                print("❌ Farmer profile not found for user")
                response_data["farmer"] = None

        return Response(response_data)
