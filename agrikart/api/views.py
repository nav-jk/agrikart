from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from farmer.models import Farmer
from buyer.models import Buyer

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
