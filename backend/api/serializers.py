from rest_framework import serializers
from farmer.models import Farmer, Produce
from buyer.models import Buyer, CartItem, Order

class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = '__all__'

class FarmerSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer(many=True, read_only=True)

    class Meta:
        model = Farmer
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Buyer
        fields = '__all__'
