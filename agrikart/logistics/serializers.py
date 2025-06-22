from rest_framework import serializers
from logistics.models import CourierAssignment

class CourierAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierAssignment
        fields = '__all__'
