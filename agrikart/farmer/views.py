from rest_framework import viewsets
from .models import Farmer, Produce
from .serializers import FarmerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from .serializers import ProduceSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Farmer


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__phone_number'
def get_object(self):
    phone = self.kwargs['user__phone_number']
    return Farmer.objects.get(user__phone_number=phone)

class ProduceViewSet(viewsets.ModelViewSet):
    serializer_class = ProduceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        farmer = Farmer.objects.get(user=self.request.user)
        queryset = Produce.objects.filter(farmer=farmer)

        # Optional filtering
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset

    def perform_create(self, serializer):
        farmer = Farmer.objects.get(user=self.request.user)
        serializer.save(farmer=farmer)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_farmer_exists(request, phone_number):
    exists = Farmer.objects.filter(user__phone_number=phone_number).exists()
    return Response({"exists": exists})


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Produce
from .serializers import ProduceNamePriceSerializer

class ProducePricingListView(APIView):
    def get(self, request):
        queryset = Produce.objects.filter(quantity__gt=0, is_active=True)
        serializer = ProduceNamePriceSerializer(queryset, many=True)
        return Response(serializer.data)
