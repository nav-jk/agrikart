from rest_framework import serializers
from .models import Buyer, CartItem, Order
from farmer.serializers import ProduceSerializer

class CartItemSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'produce', 'quantity']

class BuyerSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True, read_only=True)
    orders = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Buyer
        fields = ['id', 'address', 'cart', 'orders']

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'status']
