from rest_framework import viewsets
from farmer.models import Farmer
from buyer.models import Buyer
from .serializers import FarmerSerializer, BuyerSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import SignupSerializer

class FarmerViewSet(viewsets.ModelViewSet):
    lookup_field = 'phone_number'
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer

class BuyerViewSet(viewsets.ModelViewSet):
    lookup_field = 'phone_number'
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
