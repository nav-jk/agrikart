from rest_framework import serializers
from .models import Buyer, CartItem, Order
from farmer.serializers import ProduceSerializer
from farmer.models import Produce


class CartItemSerializer(serializers.ModelSerializer):
    produce = serializers.PrimaryKeyRelatedField(
        queryset=Produce.objects.all(),
        write_only=True
    )
    produce_info = ProduceSerializer(source='produce', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'produce', 'produce_info', 'quantity']

    def create(self, validated_data):
        buyer = self.context['request'].user.buyer
        produce = validated_data['produce']
        quantity = validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(
            buyer=buyer,
            produce=produce,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item



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

