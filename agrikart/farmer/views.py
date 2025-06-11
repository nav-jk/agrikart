from rest_framework import viewsets
from .models import Farmer
from .serializers import FarmerSerializer
from rest_framework.permissions import IsAuthenticated

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__phone_number'
def get_object(self):
    phone = self.kwargs['user__phone_number']
    return Farmer.objects.get(user__phone_number=phone)
