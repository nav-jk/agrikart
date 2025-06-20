from rest_framework import serializers
from .models import Farmer, Produce

class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = ['id', 'name', 'price', 'quantity', 'category']



class FarmerSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer(many=True, read_only=True)

    class Meta:
        model = Farmer
        fields = ['id', 'name', 'address', 'produce']

# serializers.py
from rest_framework import serializers
from .models import Produce

class ProduceNamePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = ['name', 'price']
