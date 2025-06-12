from rest_framework import viewsets
from .models import Farmer, Produce
from .serializers import FarmerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from .serializers import ProduceSerializer

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