from rest_framework import viewsets
from farmer.models import Farmer
from buyer.models import Buyer
from .serializers import FarmerSerializer, BuyerSerializer

class FarmerViewSet(viewsets.ModelViewSet):
    lookup_field = 'phone_number'
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer

class BuyerViewSet(viewsets.ModelViewSet):
    lookup_field = 'phone_number'
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
